import React from "react";
import { SnackbarProvider, MaterialDesignContent } from "notistack";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Provider } from "react-redux";
import store from "./store";
import "./App.css";
import jwt_decode from "jwt-decode";
import setAuthToken from "./utils/setAuthToken";
import PrivateRoute from "./components/common/PrivateRoute";

import { setCurrentUser, logoutUser } from "./actions/authActions";

import Landing from "./components/Landing";
import Login from "./components/auth/Login";
import Register from "./components/auth/Register";
import Dashboard from "./components/dashboard";
import BrokerSync from "./components/addtrades/brokersync";
import TradesTable from "./components/TradesTable";
import styled from "@emotion/styled";

if (localStorage.jwtToken) {
  setAuthToken(localStorage.jwtToken);
  const decoded = jwt_decode(localStorage.jwtToken);
  store.dispatch(setCurrentUser(decoded));
  const currentTime = Date.now() / 1000;
  const tokenExp = new Date(decoded.exp);
  if (tokenExp.getTime() < currentTime) {
    store.dispatch(logoutUser());
  }
}

const StyledMaterialDesignContent = styled(MaterialDesignContent)(() => ({
  "&.notistack-MuiContent-success": {
    backgroundColor: "#0094b6",
  },
}));

function App() {
  return (
    <Provider store={store}>
      <Router>
        <div className="App" style={{ backgroundColor: "whitesmoke" }}>
          <SnackbarProvider
            Components={{ success: StyledMaterialDesignContent }}
            anchorOrigin={{
              vertical: "bottom",
              horizontal: "right",
            }}
            maxSnack={5}
            preventDuplicate
          >
            <Routes>
              <Route path="/" Component={Landing} />
              <Route path="/login" Component={Login} />
              <Route path="/register" Component={Register} />
              <Route
                path="/dashboard"
                element={
                  <PrivateRoute>
                    <Dashboard />
                  </PrivateRoute>
                }
              />
              <Route
                path="/addtrades/Broker Synchronization"
                element={
                  <PrivateRoute>
                    <BrokerSync />
                  </PrivateRoute>
                }
              />
              <Route
                path="/tradestable"
                element={
                  <PrivateRoute>
                    <TradesTable />
                  </PrivateRoute>
                }
              />
            </Routes>
          </SnackbarProvider>
        </div>
      </Router>
    </Provider>
  );
}

export default App;
