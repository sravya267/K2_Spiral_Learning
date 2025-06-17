import axios from 'axios';

// Set the base URL for API requests
// In development, this will be your local server
// In production, you would replace this with your actual API URL
const API_BASE_URL = 'https://sravya1.pythonanywhere.com/api';

/**
 * Fetches the available math concepts from the backend
 * @returns {Promise} Promise that resolves to concept data
 */
export const getAvailableConcepts = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/concepts`);
    return response.data;
  } catch (error) {
    console.error('Error fetching concepts:', error);
    throw error;
  }
};

/**
 * Generates a math worksheet based on provided options
 * @param {Object} worksheetData - The worksheet configuration
 * @param {string} worksheetData.worksheet_type - 'spiral' or 'fluency'
 * @param {string} worksheetData.difficulty - 'beginner', 'intermediate', or 'advanced'
 * @param {Array} worksheetData.concepts - List of concept IDs to include
 * @param {boolean} worksheetData.include_answer_key - Whether to include an answer key
 * @param {number} worksheetData.question_count - Number of questions for fluency worksheets
 * @returns {Promise} Promise that resolves to the generated worksheet data
 */
export const generateWorksheet = async (worksheetData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/generate-worksheet`, worksheetData);
    return response.data;
  } catch (error) {
    console.error('Error generating worksheet:', error);
    throw error;
  }
};

/**
 * Helper function to download a file from a URL
 * @param {string} url - URL of the file to download
 * @param {string} filename - Name to save the file as
 */
export const downloadFile = (url, filename) => {
  // Create a link element
  const link = document.createElement('a');
  link.href = url;
  link.download = filename || 'worksheet.pdf';

  // Append to body, click, and clean up
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};