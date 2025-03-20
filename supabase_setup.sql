-- Setup script for Supabase database tables

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Access Codes Table
CREATE TABLE IF NOT EXISTS access_codes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code TEXT UNIQUE NOT NULL,
    remaining_uses INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index on code for faster lookups
CREATE INDEX IF NOT EXISTS idx_access_codes_code ON access_codes(code);

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    telegram_id BIGINT UNIQUE NOT NULL,
    telegram_username TEXT,
    access_code TEXT,
    top_values TEXT[] NOT NULL DEFAULT '{}',
    next_values TEXT[] NOT NULL DEFAULT '{}',
    schwartz_categories TEXT[] NOT NULL DEFAULT '{}',
    age INTEGER,
    country TEXT,
    occupation TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index on telegram_id for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id);

-- Values Table (for the 65 predefined values)
CREATE TABLE IF NOT EXISTS values (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    value TEXT UNIQUE NOT NULL,
    description TEXT,
    schwartz_category TEXT,
    gouveia_category TEXT
);

-- Create index on value for faster lookups
CREATE INDEX IF NOT EXISTS idx_values_value ON values(value);

-- Reports Table
CREATE TABLE IF NOT EXISTS reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    telegram_id BIGINT NOT NULL,
    sections_content JSONB NOT NULL DEFAULT '{}'::jsonb,
    prompts_used JSONB NOT NULL DEFAULT '{}'::jsonb,
    generation_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT fk_user
        FOREIGN KEY(telegram_id)
        REFERENCES users(telegram_id)
        ON DELETE CASCADE
);

-- Create index on telegram_id for faster lookups
CREATE INDEX IF NOT EXISTS idx_reports_telegram_id ON reports(telegram_id);

-- Sample Access Code Insertion
INSERT INTO access_codes (code, remaining_uses)
VALUES 
    ('DEMO123', 5),
    ('TEST456', 10)
ON CONFLICT (code) DO NOTHING;

-- Sample Values Insertion (a few examples from the 65 values)
INSERT INTO values (value, description, schwartz_category, gouveia_category)
VALUES 
    ('Achievement', 'Personal success through demonstrating competence according to social standards', 'Achievement', 'Promotion'),
    ('Benevolence', 'Preservation and enhancement of the welfare of people with whom one is in frequent personal contact', 'Benevolence', 'Interactive'),
    ('Conformity', 'Restraint of actions, inclinations, and impulses likely to upset or harm others and violate social expectations or norms', 'Conformity', 'Normative'),
    ('Hedonism', 'Pleasure and sensuous gratification for oneself', 'Hedonism', 'Excitement'),
    ('Power', 'Social status and prestige, control or dominance over people and resources', 'Power', 'Promotion'),
    ('Security', 'Safety, harmony, and stability of society, of relationships, and of self', 'Security', 'Existence'),
    ('Self-Direction', 'Independent thought and action—choosing, creating, exploring', 'Self-Direction', 'Existence'),
    ('Stimulation', 'Excitement, novelty, and challenge in life', 'Stimulation', 'Excitement'),
    ('Tradition', 'Respect, commitment, and acceptance of the customs and ideas that traditional culture or religion provide', 'Tradition', 'Normative'),
    ('Universalism', 'Understanding, appreciation, tolerance, and protection for the welfare of all people and for nature', 'Universalism', 'Suprapersonal')
ON CONFLICT (value) DO NOTHING;

-- Function to update 'updated_at' timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update 'updated_at' on users table
CREATE TRIGGER update_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column();

-- Row Level Security Policies

-- Enable RLS on all tables
ALTER TABLE access_codes ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE values ENABLE ROW LEVEL SECURITY;
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;

-- Create policies (adjust according to your authentication setup)
-- This is a basic example, you'd want to customize these based on your auth setup

-- Allow service role to do anything
CREATE POLICY "Service role can do anything on access_codes" ON access_codes FOR ALL TO service_role USING (true);
CREATE POLICY "Service role can do anything on users" ON users FOR ALL TO service_role USING (true);
CREATE POLICY "Service role can do anything on values" ON values FOR ALL TO service_role USING (true);
CREATE POLICY "Service role can do anything on reports" ON reports FOR ALL TO service_role USING (true);

-- Allow authenticated users to read values
CREATE POLICY "Authenticated users can read values" ON values FOR SELECT TO authenticated USING (true);

-- Allow users to read their own data
CREATE POLICY "Users can read their own data" ON users FOR SELECT TO authenticated USING (auth.uid()::text = telegram_id::text);
CREATE POLICY "Users can read their own reports" ON reports FOR SELECT TO authenticated USING (auth.uid()::text = telegram_id::text);