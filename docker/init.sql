-- Create databases
CREATE DATABASE auth_db;
CREATE DATABASE booking_db;
CREATE DATABASE logging_db;

-- =========================
-- auth_db
-- =========================
\connect auth_db
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO users (id, name, email, password_hash)
VALUES
    ('11111111-1111-1111-1111-111111111111', '12344321', '12344321@gmail.com', '$2b$12$Lie4pKJggxj6528fF5soN.Z2YlGT/Qq5szbS28VZjiA5aVG5fehKO')
ON CONFLICT (id) DO NOTHING;

-- =========================
-- booking_db
-- =========================
\connect booking_db
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS hotels (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    img_url VARCHAR(500),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS rooms (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    hotel_id UUID NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    room_number VARCHAR(50) NOT NULL,
    room_type INTEGER NOT NULL,
    price_per_night NUMERIC(10,2) NOT NULL,
    img_url VARCHAR(500)
);

CREATE TABLE IF NOT EXISTS bookings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    room_id UUID NOT NULL REFERENCES rooms(id) ON DELETE CASCADE,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Seed test data (hotels & rooms)
INSERT INTO hotels (id, name, location, description, img_url)
VALUES
    ('11111111-1111-1111-1111-111111111111', 'Grand Hotel', 'Москва, Красная площадь, 1', 'Роскошный отель в самом центре Москвы с видом на Кремль.', 'https://i.imgur.com/bDbrSLg.jpeg'),
    ('22222222-2222-2222-2222-222222222222', 'Seaside Resort', 'Сочи, Приморская набережная, 15', 'Современный курортный отель на берегу Чёрного моря.', 'https://i.imgur.com/uPAm5qn.jpeg'),
    ('33333333-3333-3333-3333-333333333333', 'Riders Lodge', 'Красная Поляна, Горная улица, 42', 'Уютный горный отель для любителей активного отдыха.', 'https://i.imgur.com/nMc1Rmk.jpeg')
ON CONFLICT (id) DO NOTHING;

INSERT INTO rooms (id, hotel_id, room_number, room_type, price_per_night, img_url)
VALUES
    ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '11111111-1111-1111-1111-111111111111', '101', 1, 2500.00, 'https://i.imgur.com/mOdXYNC.jpeg'),
    ('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', '11111111-1111-1111-1111-111111111111', '102', 2, 3500.00, 'https://i.imgur.com/9aGTKdl.jpeg'),
    ('cccccccc-cccc-cccc-cccc-cccccccccccc', '11111111-1111-1111-1111-111111111111', '201', 3, 5000.00, 'https://i.imgur.com/HiifPg3.jpeg'),
    ('dddddddd-dddd-dddd-dddd-dddddddddddd', '22222222-2222-2222-2222-222222222222', '101', 1, 3000.00, 'https://i.imgur.com/mOdXYNC.jpeg'),
    ('eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee', '22222222-2222-2222-2222-222222222222', '102', 2, 4500.00, 'https://i.imgur.com/9aGTKdl.jpeg'),
    ('ffffffff-ffff-ffff-ffff-ffffffffffff', '22222222-2222-2222-2222-222222222222', '301', 3, 6500.00, 'https://i.imgur.com/HiifPg3.jpeg'),
    ('00000000-0000-0000-0000-000000000001', '33333333-3333-3333-3333-333333333333', '101', 1, 2000.00, 'https://i.imgur.com/mOdXYNC.jpeg'),
    ('00000000-0000-0000-0000-000000000002', '33333333-3333-3333-3333-333333333333', '202', 2, 3000.00, 'https://i.imgur.com/9aGTKdl.jpeg')
ON CONFLICT (id) DO NOTHING;

-- =========================
-- logging_db
-- =========================
\connect logging_db
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    level INTEGER NOT NULL,
    message VARCHAR(1000) NOT NULL,
    service_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

