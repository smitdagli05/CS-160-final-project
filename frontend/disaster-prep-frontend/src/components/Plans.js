import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Plans.css'; 

function Plans() {
  const [selectedPlan, setSelectedPlan] = useState('evacuation');
  const [disasterInfo, setDisasterInfo] = useState(null);

  useEffect(() => {
    fetchDisasterInfo();
  }, []);

  const fetchDisasterInfo = async () => {
    try {
      const response = await axios.get('/api/disaster-info/user123'); // Replace 'user123' with the actual user ID
      setDisasterInfo(response.data);
    } catch (error) {
      console.error('Error fetching disaster info:', error);
    }
  };

  const handlePlanChange = (plan) => {
    setSelectedPlan(plan);
  };

  if (!disasterInfo) {
    return <div>Loading...</div>;
  }

  const { evacuation, shelter, first_aid } = disasterInfo;

  return (
    <div>
      <h2>Plans</h2>
      <div className="plan-options">
        <button
          className={selectedPlan === 'evacuation' ? 'active' : ''}
          onClick={() => handlePlanChange('evacuation')}
        >
          Evacuation
        </button>
        <button
          className={selectedPlan === 'shelter' ? 'active' : ''}
          onClick={() => handlePlanChange('shelter')}
        >
          Shelter in Place
        </button>
        <button
          className={selectedPlan === 'first_aid' ? 'active' : ''}
          onClick={() => handlePlanChange('first_aid')}
        >
          First Aid
        </button>
      </div>
      {selectedPlan && (
        <div className="plan-details">
          <h3>{selectedPlan.charAt(0).toUpperCase() + selectedPlan.slice(1)}</h3>
          <h4>What You Need</h4>
          <ul>
            {disasterInfo[selectedPlan].what_you_need.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
          <h4>Things To Keep In Mind</h4>
          <ul>
            {disasterInfo[selectedPlan].things_to_keep_in_mind.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
          <a href={disasterInfo[selectedPlan].additional_resources} target="_blank" rel="noopener noreferrer">
            Additional Resources
          </a>
        </div>
      )}
    </div>
  );
}

export default Plans;