import tomllib
import subprocess

TOML_FILE_PATH = "settings.toml"


def update_prisma():
    with open(TOML_FILE_PATH, "rb") as toml_file:
        data = tomllib.load(toml_file)
    if not data:
        raise Exception("Failed to load TOML data")

    roles = data["club_details"]["roles"]
    departments = data["club_details"]["departments"]

    roles_enum = f"""
    enum Roles {{
        {'\n    '.join(roles)}
    }}
    """

    departments_enum = f"""
    enum Departments {{
        {'\n    '.join(departments)}
    }}
    """

    with open(data["project_details"]["prisma_path"], "r") as prisma_file:
        prisma_schema = prisma_file.read()
    if not prisma_schema:
        raise Exception("Failed to read Prisma schema")

    if "enum Roles {" in prisma_schema:
        prisma_schema = prisma_schema.replace(
            prisma_schema[
                prisma_schema.find("enum Roles {") : prisma_schema.find(
                    "}", prisma_schema.find("enum Roles {")
                )
                + 1
            ],
            roles_enum.strip(),
        )
    else:
        prisma_schema += f"\n\n{roles_enum.strip()}"

    if "enum Departments {" in prisma_schema:
        prisma_schema = prisma_schema.replace(
            prisma_schema[
                prisma_schema.find("enum Departments {") : prisma_schema.find(
                    "}", prisma_schema.find("enum Departments {")
                )
                + 1
            ],
            departments_enum.strip(),
        )
    else:
        prisma_schema += f"\n\n{departments_enum.strip()}"

    with open(data["project_details"]["prisma_path"], "w") as prisma_file:
        prisma_file.write(prisma_schema)
    print("Updated Prisma schema successfully")


if __name__ == "__main__":
    update_prisma()
