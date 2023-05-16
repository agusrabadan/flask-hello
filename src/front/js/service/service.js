const URL =
  "https://3001-mmeitin-osigrisagropoin-3nqdxrxjcqf.ws-eu97.gitpod.io";
const URLCROP =
  "https://3001-mmeitin-osigrisagropoin-3nqdxrxjcqf.ws-eu97.gitpod.io/api/crop";

const HEADERS = {
  "Content-Type": "application/json",
};

export const registerFarmer = async (newUser) => {
  const raw = JSON.stringify(newUser);
  try {
    const resp = await fetch(`${URL}/api/user/signup/farmer/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: raw,
      redirect: "follow",
    });
    const data = await resp.json();
    localStorage.setItem("token", data.token);
    localStorage.setItem("role", data.role);
    
    return data;
  } catch (err) {
    console.log("Error al crear nuevo User_Farmer", err);
  }
};

export const addFarm = async (newFarm) => {
  const raw = JSON.stringify(newFarm);
  try {
    console.log("Farm created on service", newFarm);
    const resp = await fetch(`${URLCROP}/addFarm`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: raw,
      redirect: "follow",
    });
    return await resp.json();
  } catch (err) {
    console.log("Error al crear el nuevo campo", err);
  }
};
export const loginUser = async (user) => {
  try {
    const res = await fetch(`${URL}/api/user/login`, {
      method: "POST",
      headers: HEADERS,
      body: JSON.stringify(user),
    });
    const data = await res.json();

    localStorage.setItem("token", data.token);

    localStorage.setItem("role", data.role);
    return data.role;
  } catch (err) {
    console.log("ERROR LOGIN USER", err);
  }
};

export const getInfoUser = async (token) => {
  try {
    const res = await fetch(`${URL}/api/user/`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        ...HEADERS,
      },
    });
    const data = await res.json();
    return data;
  } catch (err) {
    console.log("ERROR GET USER", err);
  }
};

export const getInfoFarmer = async (id_user, token) => {
  try {
    const res = await fetch(`${URL}/api/farmer/${id_user}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        ...HEADERS,
      },
    });
    const data = await res.json();
    return data;
  } catch (err) {
    console.log("ERROR GET FARMER", err);
  }
};

export const getInfoTech = async (id_user, token) => {
  try {
    const res = await fetch(`${URL}/api/tech/${id_user}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        ...HEADERS,
      },
    });
    const data = await res.json();
    return data;
  } catch (err) {
    console.log("ERROR Get technician", err);
  }
};

export const registerTech = async (newUser) => {
  const raw = JSON.stringify(newUser);
  try {
    const resp = await fetch(`${URL}/api/user/signup/tech/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: raw,
      redirect: "follow",
    });
    const data = await resp.json();
    console.log("From service -->", data);
    localStorage.setItem("token", data.token);
    localStorage.setItem("role", data.role);

    return data;
  } catch (err) {
    console.log("Error al crear nuevo User_Tech", err);
  }
};

export const getInfoCrop = async () => {
  const token = localStorage.getItem("token");
  console.log(token);
  try {
    const res = await fetch(`${URLCROP}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        ...HEADERS,
      },
    });

    const data = await res.json();
    console.log("la data del fetch", data);
    return data;
  } catch (error) {
    console.error("Error en getInfoCrop", error);
  }
};