

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


-- ============================================================================
-- TRIGGER 2: Decrement total_check_ins on attendance delete (Bonus)
-- ============================================================================
-- This trigger decrements the counter when an attendance record is deleted
-- (useful for corrections)

-- Drop existing trigger and function if they exist
DROP TRIGGER IF EXISTS decrement_member_check_ins ON attendance;
DROP FUNCTION IF EXISTS decrement_member_check_ins_func();

-- Create the trigger function
CREATE OR REPLACE FUNCTION decrement_member_check_ins_func()
RETURNS TRIGGER AS $$
BEGIN
    -- Decrement the total_check_ins for the member
    UPDATE members
    SET total_check_ins = GREATEST(total_check_ins - 1, 0),
        updated_at = NOW()
    WHERE id = OLD.member_id;
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger
CREATE TRIGGER decrement_member_check_ins
    AFTER DELETE ON attendance
    FOR EACH ROW
    EXECUTE FUNCTION decrement_member_check_ins_func();




-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================
-- Use these queries to verify that triggers are installed correctly

-- Check if triggers exist
SELECT trigger_name, event_manipulation, event_object_table
FROM information_schema.triggers
WHERE trigger_schema = 'public'
ORDER BY event_object_table, trigger_name;

-- Check if functions exist
SELECT routine_name, routine_type
FROM information_schema.routines
WHERE routine_schema = 'public'
AND routine_type = 'FUNCTION'
AND routine_name LIKE '%check_ins%' OR routine_name LIKE '%expire%'
ORDER BY routine_name;