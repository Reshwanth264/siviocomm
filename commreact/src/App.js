import React, { useState, useEffect } from 'react';

const App = () => {
  const [zohoRecords, setZohoRecords] = useState([]);

  useEffect(() => {
    fetch('/api/zoho-records') // Assuming Flask is running on the same domain
      .then(response => response.json())
      .then(data => setZohoRecords(data))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div>
      <h1>Zoho CRM Records</h1>
      <table border="1">
        <thead>
          <tr>
            <th>Id</th>
            <th>Lead Source</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Email</th>
            <th>Phone</th>
          </tr>
        </thead>
        <tbody>
          {zohoRecords.map(record => (
            <tr key={record.id}>
              <td>{record.id}</td>
              <td>{record.Lead_Source}</td>
              <td>{record.First_Name}</td>
              <td>{record.Last_Name}</td>
              <td>{record.Email}</td>
              <td>{record.Phone}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default App;
