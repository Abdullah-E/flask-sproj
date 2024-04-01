DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS handymen CASCADE;
DROP TABLE IF EXISTS tasks CASCADE;
DROP TABLE IF EXISTS task_sub_categories CASCADE;

DROP TYPE IF EXISTS gender_enum CASCADE;
DROP TYPE IF EXISTS task_category_enum CASCADE;
DROP TYPE IF EXISTS plumber_category_enum CASCADE;
DROP TYPE IF EXISTS electrician_category_enum CASCADE;
DROP TYPE IF EXISTS carpenter_category_enum CASCADE;
DROP TYPE IF EXISTS painter_category_enum CASCADE;
DROP TYPE IF EXISTS task_status_enum CASCADE;

CREATE TYPE gender_enum AS ENUM ('MALE', 'FEMALE', 'OTHER');

-- Create enums for HandymanCategory
CREATE TYPE task_category_enum AS ENUM (
    'PLUMBER', 'ELECTRICIAN', 'CARPENTER', 'PAINTER', 'TAILOR', 'SHIFTING', 'COOK', 'MASON', 'HVAC', 'VEHICLE_MECHANIC', 'VEHICLE_ELECTRICIAN', 'HOUSE_HELP', 'CAR_WASHER', 'DRIVERS', 'BABYSITTERS', 'DOCTORS', 'REAL_ESTATE_AGENTS'
);

-- Create enums for PlumberCategory
CREATE TYPE plumber_category_enum AS ENUM (
    'WATER_LINE_REPAIR', 'DRAIN_CLEANING', 'WATER_TANK_INSTALLATION', 'FAUCET_INSTALLATION'
);

-- Create enums for ElectricianCategory
CREATE TYPE electrician_category_enum AS ENUM (
    'WIRING', 'UPS_INSTALLATION', 'SOLAR_PANEL_INSTALLATION', 'BREAKER_BOX_INSTALLATION'
);

-- Create enums for CarpenterCategory
CREATE TYPE carpenter_category_enum AS ENUM (
    'FURNITURE_REPAIR', 'FURNITURE_INSTALLATION', 'DOOR_REPAIR', 'DOOR_INSTALLATION'
);

-- Create enums for PainterCategory
CREATE TYPE painter_category_enum AS ENUM (
    'WALL_PAINTING', 'FURNITURE_PAINTING', 'WALLPAPER_INSTALLATION', 'WALLPAPER_REMOVAL'
);

-- Create enums for TaskStatus
CREATE TYPE task_status_enum AS ENUM (
    'PENDING', 'ACCEPTED', 'COMPLETED', 'CANCELLED'
);


CREATE TABLE users (
    id UUID PRIMARY KEY NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    cnic VARCHAR(15),
    gender gender_enum,
    phone_number VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    services text[],
    otp VARCHAR(4) NOT NULL,
    phone_number_verified BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE handymen (
    id UUID PRIMARY KEY NOT NULL,
    user_id UUID REFERENCES users(id) NOT NULL,
    category task_category_enum NOT NULL,
    sub_categories text[] NOT NULL,
    about VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    status boolean NOT NULL DEFAULT FALSE
);

CREATE TABLE tasks (
    id UUID PRIMARY KEY NOT NULL,
    user_id UUID REFERENCES users(id) NOT NULL,
    handyman_id UUID REFERENCES handymen(id),
    category task_category_enum NOT NULL,
    sub_categories text[] NOT NULL,
    description VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    budget integer NOT NULL,
    duration integer NOT NULL,
    date TIMESTAMP NOT NULL,
    time TIMESTAMP NOT NULL,
    status task_status_enum NOT NULL
);
