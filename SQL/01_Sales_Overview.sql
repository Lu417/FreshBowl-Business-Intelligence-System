-- ==========================================
-- Business Question 1
-- What is the total revenue generated?
-- ==========================================

SELECT
    SUM(TotalAmount) AS TotalRevenue
FROM Orders;