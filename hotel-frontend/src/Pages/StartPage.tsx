import {useNavigate} from "react-router-dom";
import {setHotelId, setRoomId} from "../redux/HotelSlice.tsx";
import {useEffect} from "react";
import {useAppDispatch} from "../redux/Hooks.tsx";

export function StartPage() {
    const navigate = useNavigate();
    const dispatch = useAppDispatch();

    useEffect(() => {
        (async () => {
            dispatch(setHotelId(""));
            dispatch(setRoomId(""));
        })();
    }, []);

    return (
        <div className="start-banner">

            <div className="text-container">
                <h1>Бронируйте номера в отелях</h1>
                <p>У нас всегда все самое выгодное</p>
                <div className="go-to-get-order" onClick={() => navigate("/hotels")}>
                    <h2>Забронировать Отель</h2>
                </div>
            </div>
        </div>
    )
}

export default StartPage;