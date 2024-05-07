import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Navigation from './Navigation';
import './Plans.css';

function Plans() {
  const [selectedPlan, setSelectedPlan] = useState(null);
  const [disasterInfo, setDisasterInfo] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [userLocation, setUserLocation] = useState(null);

  useEffect(() => {
    fetchDisasterInfo();
    getUserLocation();
  }, []);

  const fetchDisasterInfo = async () => {
    try {
      const response = await axios.get('/api/disaster-info/user123'); // Replace 'user123' with the actual user ID
      setDisasterInfo(response.data);
      setIsLoading(false);
    } catch (error) {
      console.error('Error fetching disaster info:', error);
      setIsLoading(false);
    }
  };

  const getUserLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          setUserLocation({ latitude, longitude });
        },
        (error) => {
          console.error('Error getting user location:', error);
        }
      );
    } else {
      console.error('Geolocation is not supported by this browser.');
    }
  };

  const handlePlanChange = (plan) => {
    setSelectedPlan(plan);
  };

  return (
    <div className="plans-container">
      <div className="header">Plans</div>
      <div className="plan-options">
        <div
          className={`plan-option ${selectedPlan === 'evacuation' ? 'active' : ''}`}
          onClick={() => handlePlanChange('evacuation')}
        >
          <span>Evacuation</span>
          <div className="arrow"></div>
        </div>
        <div
          className={`plan-option ${selectedPlan === 'shelter' ? 'active' : ''}`}
          onClick={() => handlePlanChange('shelter')}
        >
          <span>Shelter in Place</span>
          <div className="arrow"></div>
        </div>
        <div
          className={`plan-option ${selectedPlan === 'first aid' ? 'active' : ''}`}
          onClick={() => handlePlanChange('first aid')}
        >
          <span>First Aid</span>
          <div className="arrow"></div>
        </div>
      </div>
      {isLoading ? (
        <div className="loading">Loading...</div>
      ) : selectedPlan && disasterInfo ? (
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
          {selectedPlan === 'evacuation' && (
            <div className="evacuation-route">
              <h4>Evacuation Route</h4>
              {userLocation ? (
                <iframe
                  title="Evacuation Route"
                  width="100%"
                  height="400"
                  frameBorder="0"
                  src={`https://www.google.com/maps/embed/v1/directions?key=AIzaSyChJ6RIAcQaZkW1WNJHveCDh7a_KlhLtTo&origin=${userLocation.latitude},${userLocation.longitude}&destination=${disasterInfo.evacuation.additional_resources}&zoom=12`}
                  allowFullScreen
                ></iframe>
              ) : (
                <p>Location permission not granted. Unable to display evacuation route.</p>
              )}
            </div>
          )}
          <h4>Additional Resources</h4>
          <a href={disasterInfo[selectedPlan].additional_resources} target="_blank" rel="noopener noreferrer">
            {disasterInfo[selectedPlan].additional_resources}
          </a>
        </div>
      ) : null}
      <Navigation />
    </div>
  );
}

export default Plans;