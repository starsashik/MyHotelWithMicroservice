import {NavLink, useNavigate} from "react-router-dom";
import {setUpdate} from "../redux/UserSlice.tsx";
//import {LogoutUser} from "../api/AppApi.ts";
import {useAppDispatch, useAppSelector} from "../redux/Hooks.tsx";
import {useEffect,} from "react";

const Header = () => {
    const user = useAppSelector((state) => state.user);
    const dispatch = useAppDispatch();
    const navigate = useNavigate();
    const isLogged = user.isLoggedIn;
    const isAdminMode = user.email === "12344321@gmail.com";

    useEffect(() => {
        console.log(user.email);
    }, []);

    const handleLogout = () => {
        localStorage.removeItem("token");
        localStorage.removeItem("token_login_at");
        dispatch(setUpdate());
        navigate("/");
    };

    return (
        <header>
            <div>
                <span className="logo">
                    <NavLink to={"/home"} style={{textDecoration: "none", color: "black"}}>MyHotels</NavLink>
                </span>

                {!isLogged ? (
                    <ul className="nav">
                        <li>
                            <NavLink to={"/help"} style={{textDecoration: "none", color: "black"}}>Помощь</NavLink>
                        </li>
                        <li>
                            <NavLink to={"/login"}
                                     style={{textDecoration: "none", color: "black"}}>Авторизация</NavLink>
                        </li>
                        <li>
                            <NavLink to={"/register"}
                                     style={{textDecoration: "none", color: "black"}}>Регистрация</NavLink>
                        </li>
                    </ul>
                ) : (
                    <ul className="nav">
                        <li>
                            <NavLink to={"/help"} style={{textDecoration: "none", color: "black"}}>Помощь</NavLink>
                        </li>
                        <li>
                            <NavLink to={"/profile"}
                                     style={{textDecoration: "none", color: "black"}}>{user.email}</NavLink>
                        </li>
                        <li>
                            <NavLink to={"/bookings"} style={{textDecoration: "none", color: "black"}}>Брони</NavLink>
                        </li>
                        <li>
                            <button
                                onClick={handleLogout}
                                style={{
                                    textDecoration: "none",
                                    color: "black",
                                    background: "none",
                                    border: "none",
                                    cursor: "pointer"
                                }}>Выйти
                            </button>
                        </li>
                        <li>
                            {isAdminMode && (
                                <NavLink to={"/admin"} style={{textDecoration: "none", color: "black"}}>Панель
                                    администратора</NavLink>
                            )}
                        </li>
                    </ul>
                )}

            </div>
        </header>
    );
}

export default Header;