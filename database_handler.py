# database_handler.py

import mysql.connector
from mysql.connector import Error
from typing import Optional, Dict, Any, List, Tuple
from validators import InputValidator

class DatabaseHandler:
    def __init__(self, host: str, user: str, password: str, database: str):
        # Initialize database connection
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            print("Successfully connected to the database")
        except Error as e:
            print(f"Error connecting to the database: {e}")
            raise

        self.validator = InputValidator()

    def execute_query(self, query: str, params: tuple = None) -> Optional[List[tuple]]:
        # Execute a SQL query with error handling
        try:
            cursor = self.connection.cursor(prepared=True)
            cursor.execute(query, params)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"Error executing query: {e}")
            return None

    def get_car_location(self, car_id: int) -> Optional[Dict[str, Any]]:
        # Get car location information
        validated_car_id = self.validator.validate_car_id(car_id)
        if validated_car_id is None:
            raise ValueError("Invalid car ID format")

        query = """
        SELECT 
            ac.Warehouse_id,
            tl.Title as towing_status,
            ac.Delivered_date
        FROM ARRIVED_CAR ac
        JOIN TOWING_LIST tl ON ac.Towing_status_id = tl.Towing_list_id
        WHERE ac.Car_id = %s
        """
        result = self.execute_query(query, (validated_car_id,))
        if result and result[0]:
            return {
                'warehouse_id': result[0][0],
                'towing_status': result[0][1],
                'delivered_date': result[0][2]
            }
        return None

    def get_loading_date(self, car_id: int) -> Optional[str]:
        # Get the loading/delivery date for a specific car
        query = """
        SELECT 
            ac.Delivered_date
        FROM ARRIVED_CAR ac
        WHERE ac.Car_id = %s
        """
        result = self.execute_query(query, (car_id,))
        return result[0][0] if result and result[0] else None

    def get_payment_status(self, membership_id: str) -> Optional[Dict[str, Any]]:
        # Get payment status using membership ID
        validated_membership_id = self.validator.validate_membership_id(membership_id)
        if validated_membership_id is None:
            raise ValueError("Invalid membership ID format")

        query = """
        SELECT 
            b.Total_amount,
            b.Remaining_amount,
            CASE 
                WHEN b.Remaining_amount IS NULL OR b.Remaining_amount = 0 THEN 'Fully Paid'
                WHEN b.Remaining_amount = b.Total_amount THEN 'Unpaid'
                ELSE 'Partially Paid'
            END as payment_status
        FROM BILL b
        JOIN CUSTOMER c ON b.Customer_id = c.Customer_id
        WHERE c.Membership_id = %s
        ORDER BY b.Create_date DESC
        LIMIT 1
        """
        result = self.execute_query(query, (validated_membership_id,))
        if result and result[0]:
            return {
                'total_amount': result[0][0],
                'remaining_amount': result[0][1],
                'status': result[0][2]
            }
        return None

    def get_car_payment_info(self, car_id: int) -> Optional[Dict[str, Any]]:
        # Get car payment details
        query = """
        SELECT 
            CASE 
                WHEN a.Status = 0 THEN 'Pending'
                WHEN a.Status = 1 THEN 'In Progress'
                WHEN a.Status = 2 THEN 'Completed'
                ELSE 'Unknown'
            END as status,
            a.US_dollar_rate,
            a.Auction_transfer_rate
        FROM CAR c
        JOIN AUCTION a ON c.Auction_id = a.Auction_id
        WHERE c.Car_id = %s
        """
        result = self.execute_query(query, (car_id,))
        if result and result[0]:
            return {
                'status': result[0][0],
                'us_dollar_rate': result[0][1],
                'auction_transfer_rate': result[0][2]
            }
        return None

    def get_arrival_date(self, car_id: int) -> Optional[str]:
        # Get arrival date information
        query = """
        SELECT 
            ac.Delivered_date
        FROM ARRIVED_CAR ac
        WHERE ac.Car_id = %s
        """
        result = self.execute_query(query, (car_id,))
        return result[0][0] if result and result[0] else None

    def close_connection(self):
        """Close the database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")