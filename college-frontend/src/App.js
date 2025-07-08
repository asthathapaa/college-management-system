// App.js
import { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [students, setStudents] = useState([]);
  
  useEffect(() => {
    const fetchData = async () => {
      const token = (await axios.post('http://localhost:8000/token', 
        "username=admin&password=admin123",
        { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
      )).data.access_token;
      
      const res = await axios.get('http://localhost:8000/students/', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setStudents(res.data);
    };
    fetchData();
  }, []);

  return (
    <div>
      <h1>Students</h1>
      <ul>
        {students.map(student => (
          <li key={student.id}>{student.name} - {student.department}</li>
        ))}
      </ul>
    </div>
  );
}
export default App;
