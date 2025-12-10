import React, {ReactNode, useEffect} from 'react';
import '../styles/index.css';
import Header from "../../Components/Header.tsx";
import Footer from "../../Components/Footer.tsx";
import {useAppDispatch, useAppSelector} from "../../redux/Hooks.tsx";
import {GetCurrentUser} from "../../api/AppApi.ts";
import { setEmail, setIsLoggedIn, setUserId} from "../../redux/UserSlice.tsx";

interface LayoutProps {
    children: ReactNode;
}

const TOKEN_LIFETIME_MS = 60 * 60 * 1000; // 1 hour

export const Layout: React.FC<LayoutProps> = ({ children }) => {
    const user = useAppSelector((state) => state.user);
    const dispatch = useAppDispatch();

    const clearAuth = () => {
        localStorage.removeItem("token");
        localStorage.removeItem("token_login_at");
        dispatch(setIsLoggedIn(false));
        dispatch(setEmail(""));
        dispatch(setUserId(""));
    };

    useEffect(() => {
        const token = localStorage.getItem("token") ?? "";
        const loginAt = Number(localStorage.getItem("token_login_at") ?? "0");

        // schedule auto logout if token exists
        if (token && loginAt) {
            const elapsed = Date.now() - loginAt;
            const remaining = TOKEN_LIFETIME_MS - elapsed;
            const timer = setTimeout(clearAuth, Math.max(0, remaining));
            return () => clearTimeout(timer);
        }
    }, [dispatch, user.update]);

    useEffect(() => {
        const fetchUser = async () => {
            const token = localStorage.getItem("token") ?? "";
            const loginAt = Number(localStorage.getItem("token_login_at") ?? "0");


            if (!token || !loginAt || Date.now() - loginAt > TOKEN_LIFETIME_MS) {
                clearAuth();
                return;
            }

            if (token) {
                const res = await GetCurrentUser(token);
                console.log(res);
                if (res.Email) {
                    dispatch(setIsLoggedIn(true));
                } else {
                    dispatch(setIsLoggedIn(false));
                }
                dispatch(setEmail(res.Email || ""));
                dispatch(setUserId(res.UserId.toString() || ""));
            }
            else
            {
                dispatch(setIsLoggedIn(false));
                dispatch(setEmail(""));
                dispatch(setUserId(""));
            }
        }

        fetchUser();
    }, [dispatch, user.update]);

    return (
        <div className="layout">
            <Header />
                <main className="layout__main">{children}</main>
            <Footer />
        </div>
    );
};
