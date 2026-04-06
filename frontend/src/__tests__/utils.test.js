/**
 * Test utilities for LifeLink frontend
 */
import { describe, it, expect } from 'vitest';

// Helper function to validate blood group
const isValidBloodGroup = (group) => {
  const validGroups = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-'];
  return validGroups.includes(group);
};

// Helper function to validate email
const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// Helper function to validate phone number
const isValidPhoneNumber = (phone) => {
  const phoneRegex = /^[0-9]{10}$/;
  return phoneRegex.test(phone);
};

// Helper function to validate coordinates
const isValidCoordinates = (lat, lng) => {
  return lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180;
};

describe('Blood Group Validation', () => {
  it('should validate correct blood groups', () => {
    expect(isValidBloodGroup('O+')).toBe(true);
    expect(isValidBloodGroup('A-')).toBe(true);
    expect(isValidBloodGroup('AB+')).toBe(true);
    expect(isValidBloodGroup('B-')).toBe(true);
  });

  it('should reject invalid blood groups', () => {
    expect(isValidBloodGroup('XX')).toBe(false);
    expect(isValidBloodGroup('invalid')).toBe(false);
    expect(isValidBloodGroup('')).toBe(false);
    expect(isValidBloodGroup('O')).toBe(false);
  });
});

describe('Email Validation', () => {
  it('should validate correct emails', () => {
    expect(isValidEmail('user@example.com')).toBe(true);
    expect(isValidEmail('test.email@domain.org')).toBe(true);
  });

  it('should reject invalid emails', () => {
    expect(isValidEmail('invalid')).toBe(false);
    expect(isValidEmail('user@')).toBe(false);
    expect(isValidEmail('@example.com')).toBe(false);
    expect(isValidEmail('')).toBe(false);
  });
});

describe('Phone Number Validation', () => {
  it('should validate correct phone numbers', () => {
    expect(isValidPhoneNumber('9876543210')).toBe(true);
    expect(isValidPhoneNumber('1234567890')).toBe(true);
  });

  it('should reject invalid phone numbers', () => {
    expect(isValidPhoneNumber('123')).toBe(false);
    expect(isValidPhoneNumber('12345')).toBe(false);
    expect(isValidPhoneNumber('abcdefghij')).toBe(false);
    expect(isValidPhoneNumber('')).toBe(false);
  });
});

describe('Coordinates Validation', () => {
  it('should validate correct coordinates', () => {
    expect(isValidCoordinates(12.9716, 77.5946)).toBe(true);
    expect(isValidCoordinates(0, 0)).toBe(true);
    expect(isValidCoordinates(-12.9716, -77.5946)).toBe(true);
    expect(isValidCoordinates(90, 180)).toBe(true);
  });

  it('should reject invalid coordinates', () => {
    expect(isValidCoordinates(91, 77)).toBe(false);
    expect(isValidCoordinates(12, 181)).toBe(false);
    expect(isValidCoordinates(-91, 77)).toBe(false);
    expect(isValidCoordinates(12, -181)).toBe(false);
  });
});

// Export utilities for use in other tests
export { isValidBloodGroup, isValidEmail, isValidPhoneNumber, isValidCoordinates };
