import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import ScrollToTop from "./component/scrollToTop";

import { Home } from "./pages/home";
import injectContext from "./store/appContext";

import Navbar from "./component/navbar";
import { Footer } from "./component/footer";

import Login from "./pages/login";
import AdminCasino from "./pages/adminCasino";
import MenuCasino from "./pages/menuCasino";
import ResumenPanelAdmin from "./pages/adminAdmin";
import PasswordRecoveryEmail from "./pages/passwordRecovery";
import PerfilUsuario from "./pages/perfilUsuario";
import PerfilEmpresa from "./pages/perfilEmpresa";
import PerfilCasino from "./pages/perfilCasino";

//create your first component
const Layout = () => {
  //the basename is used when your project is published in a subdirectory and not in the root of the domain
  // you can set the basename on the .env file located at the root of this project, E.g: BASENAME=/react-hello-webapp/
  const basename = process.env.BASENAME || "";

  return (
    <div>
      <BrowserRouter basename={basename}>
        <ScrollToTop>
          <Navbar />
          <Routes>
            <Route element={<PerfilCasino />} path="/casino"></Route>
            <Route element={<PerfilEmpresa />} path="/empresa"></Route>
            <Route element={<PerfilUsuario />} path="/user"></Route>
            <Route element={<PasswordRecoveryEmail />} path="/recovery"></Route>
            <Route element={<ResumenPanelAdmin />} path="/admin"></Route>
            <Route element={<MenuCasino />} path="/menu-casino"></Route>
            <Route element={<AdminCasino />} path="/admin-casino"></Route>
            <Route element={<Login />} path="/login"></Route>
            <Route element={<Home />} path="/" />
            <Route element={<h1>Not found!</h1>} />
          </Routes>
          <Footer />
        </ScrollToTop>
      </BrowserRouter>
    </div>
  );
};

export default injectContext(Layout);
