import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import {useAppSelector} from "../redux/Hooks.tsx";

interface PrivateRouteProps {
    IsAdmin: boolean;
}

const PrivateRoute: React.FC<PrivateRouteProps> = ({IsAdmin}) => {
    const user = useAppSelector((state) => state.user);

    if (user === undefined) {
        //return <Navigate to="/login"/>;
        return <p>Loading…</p>;
    }

    if (IsAdmin && user.email != "12344321@gmail.com")
    {
        return <Navigate to="/home"/>;
    }
    if (user == null || user.email == "") {
        return <Navigate to="/login"/>;
    }

    return <Outlet />;
};

export default PrivateRoute;
