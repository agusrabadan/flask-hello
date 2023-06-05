import React from "react";
import Input from "../input/index.jsx";
const ProfileForm = ({ handleChange, handleClick, user }) => {
  return (
    <div>
      <form onChange={handleChange} onSubmit={handleClick}>
        <Input
          icon={<i className="fa-solid fa-circle-user"></i>}
          type="text"
          placeholder="Username"
          name="username"
          defaultValue={user?.username}
        />
        <Input
          icon={<i className="fa-solid fa-circle-user"></i>}
          type="text"
          placeholder="First name"
          name="firstname"
          defaultValue={user?.firstname}
        />
        <Input
          icon={<i className="fa-solid fa-circle-user"></i>}
          type="text"
          placeholder="Last name"
          name="lastname"
          defaultValue={user?.lastname}
        />
        <Input
          icon={<i className="fa-solid fa-envelope"></i>}
          type="email"
          placeholder="Email"
          name="email"
          defaultValue={user?.email}
        />
        <button type="submit" className="submitBtn boxShadow">
          Update
        </button>
      </form>
    </div>
  );
};

export default ProfileForm;