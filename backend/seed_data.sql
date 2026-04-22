-- seed_data.sql – sample transactions for testing
-- Run after alembic upgrade head

INSERT INTO transactions (amount, description, transaction_type, category, auto_tagged, timestamp, note) VALUES
( 50000.00, 'Monthly Salary',       'income',  'Salary',        1, datetime('now', '-15 days'), 'April salary'),
( -1200.00, 'Zomato order',         'expense', 'Food',          1, datetime('now', '-14 days'), 'Dinner'),
( -3500.00, 'Amazon purchase',      'expense', 'Shopping',      1, datetime('now', '-13 days'), 'New headphones'),
( -15000.00,'Rent payment',         'expense', 'Housing',       1, datetime('now', '-12 days'), 'April rent'),
(  -500.00, 'Uber ride',            'expense', 'Transport',     1, datetime('now', '-10 days'), NULL),
(  -799.00, 'Netflix subscription', 'expense', 'Entertainment', 1, datetime('now', '-9 days'),  NULL),
( 5000.00,  'Freelance project',    'income',  'Salary',        1, datetime('now', '-7 days'),  'Logo design'),
( -800.00,  'McDonald burger',      'expense', 'Food',          1, datetime('now', '-6 days'),  NULL),
( -250.00,  'Metro card recharge',  'expense', 'Transport',     1, datetime('now', '-5 days'),  NULL),
( -599.00,  'Spotify premium',      'expense', 'Entertainment', 1, datetime('now', '-3 days'),  NULL),
( -2000.00, 'Electricity bill',     'expense', 'Housing',       1, datetime('now', '-2 days'),  'Monthly bill'),
( -400.00,  'Swiggy breakfast',     'expense', 'Food',          1, datetime('now', '-1 days'),  NULL);

INSERT INTO budgets (category, monthly_limit) VALUES
('Food',          3000.00),
('Transport',     1500.00),
('Entertainment', 1000.00),
('Shopping',      5000.00),
('Housing',       20000.00);

INSERT INTO recurring_transactions (description, amount, transaction_type, category, frequency, next_due_date) VALUES
('Netflix subscription', 799.00, 'expense', 'Entertainment', 'monthly', date('now', '+1 month')),
('Monthly Salary',       50000.00, 'income', 'Salary',       'monthly', date('now', '+1 month')),
('Spotify premium',      599.00, 'expense', 'Entertainment', 'monthly', date('now', '+1 month'));
