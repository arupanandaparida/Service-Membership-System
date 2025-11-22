

-- ============================================================================
-- TRIGGER 1: Increment total_check_ins on attendance insert
-- ============================================================================
-- This trigger automatically updates the total_check_ins counter in the members
-- table whenever a new attendance record is created

-- Drop existing trigger and function if they exist
DROP TRIGGER IF EXISTS increment_member_check_ins ON attendance;
DROP FUNCTION IF EXISTS increment_member_check_ins_func();

-- Create the trigger function
CREATE OR REPLACE FUNCTION increment_member_check_ins_func()
RETURNS TRIGGER AS $$
BEGIN
    -- Increment the total_check_ins for the member
    UPDATE members
    SET total_check_ins = total_check_ins + 1,
        updated_at = NOW()
    WHERE id = NEW.member_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger
CREATE TRIGGER increment_member_check_ins
    AFTER INSERT ON attendance
    FOR EACH ROW
    EXECUTE FUNCTION increment_member_check_ins_func();

-- =============================================
-- PostgreSQL Trigger Implementation
-- =============================================
-- This trigger automatically increments the total_check_ins
-- counter in the members table whenever a new attendance
-- record is created.

-- Step 1: Create the trigger function
CREATE OR REPLACE FUNCTION increment_member_check_ins()
RETURNS TRIGGER AS $$
BEGIN
    -- Increment total_check_ins for the member
    UPDATE members
    SET total_check_ins = total_check_ins + 1
    WHERE id = NEW.member_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Step 2: Create the trigger
DROP TRIGGER IF EXISTS attendance_insert_trigger ON attendance;

CREATE TRIGGER attendance_insert_trigger
AFTER INSERT ON attendance
FOR EACH ROW
EXECUTE FUNCTION increment_member_check_ins();


-- =============================================
-- SQLite Trigger Implementation (Alternative)
-- =============================================
-- If using SQLite instead of PostgreSQL, use this trigger:
-- (Comment out the PostgreSQL version above)

/*
DROP TRIGGER IF EXISTS attendance_insert_trigger;

CREATE TRIGGER attendance_insert_trigger
AFTER INSERT ON attendance
FOR EACH ROW
BEGIN
    UPDATE members
    SET total_check_ins = total_check_ins + 1
    WHERE id = NEW.member_id;
END;
*/

-- =============================================
-- How to Apply This Trigger
-- =============================================
-- For PostgreSQL:
--   1. Connect to your database: psql -U username -d database_name
--   2. Run: \i triggers.sql
--   Or: psql -U username -d database_name -f triggers.sql
--
-- For SQLite:
--   1. Connect to your database: sqlite3 membership_system.db
--   2. Run: .read triggers.sql
--   Or: sqlite3 membership_system.db < triggers.sql

-- =============================================
-- Testing the Trigger
-- =============================================
-- Test with these SQL commands:
--
-- 1. Check current total_check_ins:
--    SELECT id, name, total_check_ins FROM members WHERE id = 1;
--
-- 2. Insert a new attendance record:
--    INSERT INTO attendance (member_id, check_in_time) 
--    VALUES (1, CURRENT_TIMESTAMP);
--
-- 3. Verify total_check_ins was incremented:
--    SELECT id, name, total_check_ins FROM members WHERE id = 1;