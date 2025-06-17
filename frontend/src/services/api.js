/**
 * API service for communicating with the Math Worksheet Generator backend
 */

const API_BASE_URL = process.env.REACT_APP_API_URL;

console.log('API_BASE_URL:', API_BASE_URL);

/**
 * Fetches all available math concepts from the backend
 * @returns {Promise<Object>} - Object containing concept categories
 */
export const fetchConcepts = async () => {
  try {
    console.log('Fetching concepts from:', `${API_BASE_URL}/concepts`);
    const response = await fetch(`${API_BASE_URL}/concepts`);
    
    console.log('Response status:', response.status);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch concepts: ${response.status}`);
    }
    
    const data = await response.json();
    console.log('Concepts fetched successfully:', data);
    return data;
  } catch (error) {
    console.error('Error fetching concepts:', error);
    throw error;
  }
};

/**
 * Generates a math worksheet based on user selections
 * @param {Object} worksheetData - The worksheet configuration
 * @param {string} worksheetData.worksheet_type - "spiral" or "fluency"
 * @param {string} worksheetData.number_range - "beginner", "intermediate", or "advanced"
 * @param {Array<string>} worksheetData.concepts - Selected math concepts
 * @param {boolean} worksheetData.include_answer_key - Whether to include answer key
 * @returns {Promise<Blob>} - PDF blob for download
 */
export const generateWorksheet = async (worksheetData) => {
  try {
    console.log('Generating worksheet with data:', worksheetData);
    
    // Create a modified copy of the data
    const requestData = {
      ...worksheetData,
      // Map number_range to difficulty
      difficulty: worksheetData.number_range,
      // Rename problem_count to question_count if it exists
      question_count: worksheetData.problem_count || 15
    };
    
    // Remove fields that the backend doesn't expect
    delete requestData.number_range;
    delete requestData.problem_count;
    
    console.log('Sending request to:', `${API_BASE_URL}/api/generate-worksheet`);
    console.log('Request data:', requestData);
    
    // Use the correct API endpoint
    const response = await fetch(`${API_BASE_URL}/api/generate-worksheet`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData)
    });
    
    console.log('Generate worksheet response status:', response.status);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(errorData?.detail || 'Failed to generate worksheet');
    }
    
    // The response now contains a download URL
    const data = await response.json();
    console.log('Received download URL:', data.download_url);
    
    // Make a second request to get the actual PDF
    console.log('Downloading PDF from:', `${API_BASE_URL}${data.download_url}`);
    const pdfResponse = await fetch(`${API_BASE_URL}${data.download_url}`);
    
    if (!pdfResponse.ok) {
      throw new Error('Failed to download worksheet');
    }
    
    return await pdfResponse.blob();
  } catch (error) {
    console.error('Error generating worksheet:', error);
    throw error;
  }
};

/**
 * Downloads a generated worksheet as a PDF
 * @param {Blob} blob - The PDF blob
 * @param {string} filename - Name for the downloaded file
 */
export const downloadWorksheetPDF = (blob, filename = 'math_worksheet.pdf') => {
  // Create a URL for the blob
  const url = URL.createObjectURL(blob);
  
  // Create a temporary anchor element
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  
  // Programmatically click the link to trigger the download
  document.body.appendChild(link);
  link.click();
  
  // Clean up
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};