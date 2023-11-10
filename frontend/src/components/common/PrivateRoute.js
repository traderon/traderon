import React from "react";
import { Navigate } from "react-router-dom";

export default function PrivateRoute({ children }) {
  // const auth = useSelector((store) => store.auth);
  return localStorage.jwtToken ? <>{children}</> : <Navigate to="/login" />;
}
