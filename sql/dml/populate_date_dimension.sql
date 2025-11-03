SET search_path TO ecommerce_dw;

TRUNCATE TABLE dim_date;

INSERT INTO dim_date (
    date_id,
    full_date,
    day_of_week,
    day_name,
    day_of_month,
    day_of_year,
    week_of_year,
    month_number,
    month_name,
    month_abbr,
    quarter,
    quarter_name,
    year,
    is_weekend,
    is_holiday,
    fiscal_year,
    fiscal_quarter,
    fiscal_month,
    year_month,
    year_quarter
)
SELECT 
    TO_CHAR(date_series, 'YYYMMDD'):: INTEGER AS date_id,
    date_series AS full_date,
    EXTRACT(ISODOW FROM date_series):: INTEGER AS day_of_week,
    TO_CHAR(date_series, 'Day') AS day_name,
    EXTRACT(DAY FROM date_series)::INTEGER AS day_of_month,
    EXTRACT(DOY FROM date_series):: INTEGER AS day_of_year,
    EXTRACT(WEEK FROM date_series)::INTEGER AS week_of_year,
    EXTRACT(MONTH FROM date_series)::INTEGER AS month_number,
    TO_CHAR(date_series, 'Month') AS month_name,
    TO_CHAR(date_series, 'Mon') AS month_abbr,
    EXTRACT(QUARTER FROM date_series)::INTEGER AS quarter,
    'Q' || EXTRACT(QUARTER FROM date_series)::TEXT AS quarter_name,
    EXTRACT(YEAR FROM date_series)::INTEGER as year,
    CASE WHEN EXTRACT(ISODOW FROM date_series) IN (6,7) THEN TRUE ELSE FALSE END AS is_weekend,
    FALSE AS is_holiday,
    CASE
        WHEN EXTRACT(MONTH FROM date_series) >=4 THEN EXTRACT(YEAR FROM date_series)::INTEGER
        ELSE EXTRACT(YEAR FROM date_series)::INTEGER - 1
    END AS fiscal_year,
    CASE
        WHEN EXTRACT(MONTH FROM date_series) IN (4,5,6) THEN 1
        WHEN EXTRACT(MONTH FROM date_series) IN (7,8,9) THEN 2
        WHEN EXTRACT(MONTH FROM date_series) IN (10,11,12) THEN 3
        ELSE 4
    END AS fiscal_quarter,
    CASE
        WHEN EXTRACT(MONTH FROM date_series) >= 4 THEN EXTRACT(MONTH FROM date_sereis)::INTEGER -3
        ELSE EXTRACT(MONTH FROM date_sereis)::INTEGER+9
    END AS fiscal_month,
    TO_CHAR(date_series, 'YYYY-MM') AS year_month,
    EXTRACT(YEAR FROM date_series)::TEXT || '-Q' || EXTRACT(QUARTER FROM date_series)::TEXT AS year_quarter
    FROM generate_series(
        '2020-01-01'::DATE,
        '2030-12-31'::DATE,
        '1 day'::INTERVAL
    ) AS date_series;


    UPDATE dim_date SET is_holiday = TRUE, holiday_name = 'New Year''s Day' WHERE
    month_number = 1 AND day_of_month = 1;

    UPDATE dim_date SET is_holiday = TRUE, holiday_name = 'Independence Day' WHERE
    month_number = 7 AND day_of_month = 4;

    UPDATE dim_date SET is_holiday = TRUE, holiday_name = 'Christmas Day' WHERE
    month_number = 12 AND day_of_month = 25;

    UPDATE dim_date SET is_holiday = TRUE, holiday_name = 'Thanksgiving' WHERE
    month_number = 11
        AND day_name = 'Thursday'
        AND day_of_month = BETWEEN 22 AND 28;

    UPDATE dim_date SET is_holiday = TRUE, holiday_name = 'Memorial Day'
    WHERE month_number = 5
        AND day_name = 'Monday'
        AND day_of_month BETWEEN 25 AND 31;
    
    UPDATE dim_date SET is_holiday = TRUE, holiday_name = 'Labor Day'
    WHERE month_number = 9
        AND day_name = 'Monday'
        AND day_of_month BETWEEN 1 AND 7;

    SELECT 
        COUNT(*) as total_dates,
        MIN(full_date) as earliest_date,
        MAX(full_date) as latest_date,
        COUNT(*) FILTER (WHERE is_holiday = TRUE) as holiday_count,
        COUNT(*) FILTER(WHERE is_weekend = TRUE) as weekend_count
    FROM dim_date;

    SELECT * FROM dim_date 
    WHERE year = 2024 AND month_number = 1
    ORDER BY full_date
    LIMIT 10;