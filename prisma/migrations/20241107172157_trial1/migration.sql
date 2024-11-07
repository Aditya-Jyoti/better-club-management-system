/*
  Warnings:

  - You are about to drop the column `email` on the `User` table. All the data in the column will be lost.

*/
-- DropForeignKey
ALTER TABLE "Auth" DROP CONSTRAINT "Auth_id_email_fkey";

-- DropIndex
DROP INDEX "Auth_id_email_key";

-- DropIndex
DROP INDEX "User_email_key";

-- DropIndex
DROP INDEX "User_id_email_key";

-- AlterTable
ALTER TABLE "User" DROP COLUMN "email";

-- AddForeignKey
ALTER TABLE "Auth" ADD CONSTRAINT "Auth_id_fkey" FOREIGN KEY ("id") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
