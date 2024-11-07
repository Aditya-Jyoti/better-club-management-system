-- CreateEnum
CREATE TYPE "Roles" AS ENUM ('UPPER_MANAGEMENT', 'DEPARTMENT_LEADS', 'JUNIOR_DEPARTMENT_LEADS', 'MEMBER');

-- CreateEnum
CREATE TYPE "Departments" AS ENUM ('TECHNICAL', 'MANAGEMENT', 'SOCIAL_MEDIA', 'DESIGN');

-- CreateTable
CREATE TABLE "Auth" (
    "id" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "last_login" TIMESTAMP(3),
    "hashed_password" TEXT NOT NULL,
    "email" TEXT NOT NULL,

    CONSTRAINT "Auth_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "User" (
    "id" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "first_name" TEXT,
    "last_name" TEXT,
    "phone" INTEGER,
    "role" "Roles",
    "department" "Departments",

    CONSTRAINT "User_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Auth_hashed_password_key" ON "Auth"("hashed_password");

-- CreateIndex
CREATE UNIQUE INDEX "Auth_email_key" ON "Auth"("email");

-- CreateIndex
CREATE UNIQUE INDEX "Auth_id_email_key" ON "Auth"("id", "email");

-- CreateIndex
CREATE UNIQUE INDEX "User_email_key" ON "User"("email");

-- CreateIndex
CREATE UNIQUE INDEX "User_id_email_key" ON "User"("id", "email");

-- AddForeignKey
ALTER TABLE "Auth" ADD CONSTRAINT "Auth_id_email_fkey" FOREIGN KEY ("id", "email") REFERENCES "User"("id", "email") ON DELETE RESTRICT ON UPDATE CASCADE;
