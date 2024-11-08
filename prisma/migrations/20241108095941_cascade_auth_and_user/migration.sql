-- DropForeignKey
ALTER TABLE "Auth" DROP CONSTRAINT "Auth_id_email_fkey";

-- AddForeignKey
ALTER TABLE "Auth" ADD CONSTRAINT "Auth_id_email_fkey" FOREIGN KEY ("id", "email") REFERENCES "User"("id", "email") ON DELETE CASCADE ON UPDATE CASCADE;
