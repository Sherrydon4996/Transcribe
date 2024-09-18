import hashlib
import streamlit as st
import string
import MySQLdb
import os
import string


def validate_email(user_email):
    try:
        part1, part2 = user_email.split("@")
        if len(part1) > 3 and part2[-4:] == ".com":
            return True
        else:
            return False
    except ValueError:
        return False


def hashing_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def empty_fields_alert(empty_fields):
    for field in empty_fields:
        if field == "":
            return False
        return True


def validate_password(password):
    if len(password) > 6:
        return True
    return False

