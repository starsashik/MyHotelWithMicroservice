import {useEffect} from "react";
import {useAppDispatch, useAppSelector} from "../redux/Hooks.tsx";
import './styles/index.css';
import {GetCurrentUser} from "../api/AppApi.ts";
import {setAccessLvl, setEmail, setIsLoggedIn, setToken, setUserId} from "../redux/UserSlice.tsx";
import {setHotelId, setRoomId} from "../redux/HotelSlice.tsx";
import {AppRouter} from "./router/AppRouter.tsx";
import {Layout} from "./layout/LayoutMain.tsx";
import {Providers} from "./providers/Providers.tsx";

function App() {
    return (
        <div className='wrapper'>
            <Providers>
                <Layout>
                    <AppRouter/>
                </Layout>
            </Providers>
        </div>
    )
}

export default App
