import { Routes, Route, Navigate } from 'react-router-dom';
import HotelsPage from "../../Pages/HotelsPage.tsx";
import Registration from "../../Pages/RegistrationPage.tsx";
import LoginPage from "../../Pages/LoginPage.tsx";
import PrivateRoute from "../../Components/PrivateRoute.tsx";
import '../styles/index.css';
import StartPage from "../../Pages/StartPage.tsx";
import AdminPage from "../../Pages/AdminPage.tsx";
import ProfilePage from "../../Pages/ProfilePage.tsx";
import BookingsPage from "../../Pages/BookingsPage.tsx";
import RoomsPage from "../../Pages/RoomsPage.tsx";

export const AppRouter = () => {
    return (
        <Routes>
            <Route path="/" element={<Navigate to="/home"/>}/>

            <Route path="/home" element={
                <StartPage/>
            }/>

            <Route path={'/register'} element={
                <Registration/>}
            />
            <Route path={'/login'} element={
                <LoginPage/>}
            /> 

            <Route element={<PrivateRoute IsAdmin={true}/>}>
                <Route path={'/admin'} element={
                    <AdminPage/>}
                />
            </Route>

            <Route element={<PrivateRoute IsAdmin={false}/>}>
                <Route path="/hotels" element={
                    <HotelsPage/>}
                />
            </Route>

            <Route element={<PrivateRoute IsAdmin={false}/>}>
                <Route path="/profile" element={
                    <ProfilePage/>}
                />
            </Route>

            <Route element={<PrivateRoute IsAdmin={false}/>}>
                <Route path="/bookings" element={
                    <BookingsPage/>}
                />
            </Route>

            <Route element={<PrivateRoute IsAdmin={false}/>}>
                <Route path="/rooms" element={
                    <RoomsPage/>}
                />
            </Route>

            <Route path="/help" element={
                <div className="help">
                    <h1>Популярные вопросы:</h1>
                    <br/><br/>
                    <h3>Если возникнут какие-либо ошибки - вы увидите соответствующее сообщение. Если проблема в
                        сведениях заказа, то перепроверьте их корректность еще раз. Если же нет
                        то свяжитесь с администратором системы по телефону 8(800)555-35-35, и сообщите о данной
                        проблеме.</h3>
                    <br/>
                </div>
            }/>

            <Route path="*" element={<Navigate to="/home"/>}/>
        </Routes>
    );
};