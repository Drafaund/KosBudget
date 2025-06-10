# services/auth_service.py

import hashlib
import streamlit as st
from config.database import DatabaseManager
from datetime import datetime

class AuthService:
    """Service untuk handle authentication dan user management"""
    
    @staticmethod
    def hash_password(password):
        """
        Hash password menggunakan SHA-256
        
        Args:
            password (str): Plain text password
            
        Returns:
            str: Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password, hashed_password):
        """
        Verify password dengan hash
        
        Args:
            password (str): Plain text password
            hashed_password (str): Hashed password dari database
            
        Returns:
            bool: True jika password cocok
        """
        return AuthService.hash_password(password) == hashed_password
    
    @staticmethod
    def register_user(username, password):
        """
        Register user baru
        
        Args:
            username (str): Username
            password (str): Plain text password
            
        Returns:
            tuple: (success, message)
        """
        # Validasi input
        if not username or not password:
            return False, "Username dan password tidak boleh kosong"
        
        if len(username) < 3:
            return False, "Username minimal 3 karakter"
        
        if len(password) < 6:
            return False, "Password minimal 6 karakter"
        
        # Cek apakah username sudah ada
        check_query = "SELECT user_id FROM users WHERE username = %s"
        success, result = DatabaseManager.execute_query(check_query, (username,), fetch=True)
        
        if not success:
            return False, f"Error checking username: {result}"
        
        if result:  # Username sudah ada
            return False, "Username sudah digunakan"
        
        # Hash password
        hashed_password = AuthService.hash_password(password)
        
        # Insert user baru
        insert_query = """
            INSERT INTO users (username, password, created_at, updated_at) 
            VALUES (%s, %s, %s, %s)
        """
        current_time = datetime.now()
        
        success, result = DatabaseManager.execute_query(
            insert_query, 
            (username, hashed_password, current_time, current_time)
        )
        
        if success:
            return True, "Registrasi berhasil! Silakan login."
        else:
            return False, f"Error registrasi: {result}"
    
    @staticmethod
    def authenticate_user(username, password):
        """
        Authenticate user login
        
        Args:
            username (str): Username
            password (str): Plain text password
            
        Returns:
            tuple: (success, message, user_data)
        """
        # Validasi input
        if not username or not password:
            return False, "Username dan password tidak boleh kosong", None
        
        # Cari user di database
        query = "SELECT user_id, username, password FROM users WHERE username = %s"
        success, result = DatabaseManager.execute_query(query, (username,), fetch=True)
        
        if not success:
            return False, f"Error database: {result}", None
        
        if not result:  # User tidak ditemukan
            return False, "Username atau password salah", None
        
        user_data = result[0]  # result adalah list of dict
        
        # Verify password
        if AuthService.verify_password(password, user_data['password']):
            # Login berhasil
            user_info = {
                'user_id': user_data['user_id'],
                'username': user_data['username']
            }
            return True, "Login berhasil!", user_info
        else:
            return False, "Username atau password salah", None
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Get user data by user_id
        
        Args:
            user_id (int): User ID
            
        Returns:
            tuple: (success, user_data)
        """
        query = "SELECT user_id, username, created_at FROM users WHERE user_id = %s"
        success, result = DatabaseManager.execute_query(query, (user_id,), fetch=True)
        
        if success and result:
            return True, result[0]
        else:
            return False, None
    
    @staticmethod 
    def change_password(user_id, old_password, new_password):
        """
        Change user password
        
        Args:
            user_id (int): User ID
            old_password (str): Current password
            new_password (str): New password
            
        Returns:
            tuple: (success, message)
        """
        # Validasi new password
        if len(new_password) < 6:
            return False, "Password baru minimal 6 karakter"
        
        # Get current password hash
        query = "SELECT password FROM users WHERE user_id = %s"
        success, result = DatabaseManager.execute_query(query, (user_id,), fetch=True)
        
        if not success or not result:
            return False, "User tidak ditemukan"
        
        current_hash = result[0]['password']
        
        # Verify old password
        if not AuthService.verify_password(old_password, current_hash):
            return False, "Password lama salah"
        
        # Update password
        new_hash = AuthService.hash_password(new_password)
        update_query = "UPDATE users SET password = %s, updated_at = %s WHERE user_id = %s"
        
        success, result = DatabaseManager.execute_query(
            update_query, 
            (new_hash, datetime.now(), user_id)
        )
        
        if success:
            return True, "Password berhasil diubah"
        else:
            return False, f"Error mengubah password: {result}"