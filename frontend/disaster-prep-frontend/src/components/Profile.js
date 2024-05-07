import React, { useState } from 'react';
import axios from 'axios';
import Navigation from './Navigation';
import './Profile.css';

function Profile() {
  const [profile, setProfile] = useState({
    homeAddress: {
      state: '',
      city: '',
      street: '',
    },
    contactInfo: {
      primaryContact: '',
      emergencyContact: '',
    },
    considerations: '',
  });

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    if (name.startsWith('homeAddress')) {
      setProfile((prevProfile) => ({
        ...prevProfile,
        homeAddress: {
          ...prevProfile.homeAddress,
          [name.split('.')[1]]: value,
        },
      }));
    } else if (name.startsWith('contactInfo')) {
      setProfile((prevProfile) => ({
        ...prevProfile,
        contactInfo: {
          ...prevProfile.contactInfo,
          [name.split('.')[1]]: value,
        },
      }));
    } else if (name === 'considerations') {
      setProfile((prevProfile) => ({
        ...prevProfile,
        considerations: value,
      }));
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('/api/profile', {
        user_id: 'user123', // Replace with the actual user ID
        home_address: profile.homeAddress,
        contact_info: profile.contactInfo,
        considerations: profile.considerations,
      });
      console.log('Profile updated successfully:', response.data);
      // TODO: Handle success, show a success message, or redirect to another page
    } catch (error) {
      console.error('Error updating profile:', error);
      // TODO: Handle error, show an error message to the user
    }
  };

  return (
    <div className="profile-container">
      <div className="header">Profile</div>
      <form className="profile-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label>State:</label>
          <input
            type="text"
            name="homeAddress.state"
            value={profile.homeAddress.state}
            onChange={handleInputChange}
          />
        </div>
        <div className="form-group">
          <label>City:</label>
          <input
            type="text"
            name="homeAddress.city"
            value={profile.homeAddress.city}
            onChange={handleInputChange}
          />
        </div>
        <div className="form-group">
          <label>Street:</label>
          <input
            type="text"
            name="homeAddress.street"
            value={profile.homeAddress.street}
            onChange={handleInputChange}
          />
        </div>
        <div className="form-group">
          <label>Primary Contact:</label>
          <input
            type="text"
            name="contactInfo.primaryContact"
            value={profile.contactInfo.primaryContact}
            onChange={handleInputChange}
          />
        </div>
        <div className="form-group">
          <label>Emergency Contact:</label>
          <input
            type="text"
            name="contactInfo.emergencyContact"
            value={profile.contactInfo.emergencyContact}
            onChange={handleInputChange}
          />
        </div>
        <div className="form-group">
          <label>Do you want us to keep anything specific in mind for your emergency plans?</label>
          <input type="text" name="considerations" value={profile.considerations} onChange={handleInputChange} />
        </div>
        <button type="submit">Update Profile</button>
      </form>
      <Navigation />
    </div>
  );
}

export default Profile;