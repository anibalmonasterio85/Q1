-- Fix for accesos_log table: Allow user_id to be NULL
-- This allows logging access attempts for unregistered QR codes

-- IMPORTANT: Execute this immediately to fix the scanner validation errors
-- Error: "Column 'user_id' cannot be null"

USE qr_access;

-- 1. Modify user_id column to be nullable (CRITICAL)
ALTER TABLE accesos_log MODIFY COLUMN user_id INT NULL;

-- 2. Add detalles column if it doesn't exist (for storing error messages)
ALTER TABLE accesos_log ADD COLUMN IF NOT EXISTS detalles TEXT NULL;

-- Verify the changes
SHOW CREATE TABLE accesos_log;
