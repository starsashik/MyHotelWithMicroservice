import {useEffect, useState} from "react";
import {Booking, getBookings} from "../api/AppApi.ts";
import '../css/BookingsPage.css';
import {useAppSelector} from "../redux/Hooks.tsx";
import BookingCardToPage from "./Components/BookingCardToPage.tsx";
import {useNavigate} from "react-router-dom";

export function BookingsPage() {
    const hotel = useAppSelector((state)=>state.hotel);
    const navigate = useNavigate();
    const [FilteredBookings, setFilteredBookings] = useState<Booking[]>([]);
    const [errorMessage, setErrorMessage] = useState<string>("");

    useEffect(() => {
        (async () => {
            try {
                const response = await getBookings(localStorage.getItem("token") ?? "");

                console.error(response)
                setFilteredBookings(response);

                setErrorMessage('');
            } catch (error: any) {
                if (error.name === "401") {
                    setErrorMessage('Неверный токен');
                } else {
                    setErrorMessage(`Произошла ошибка: ${error.message}`);
                }
            }
        })();
    }, [hotel.numberBookings]);

    return (
        <div className="bookings-page">
            <h1 style={{display: 'flex', alignItems: 'Left', justifyContent: 'Left', gap: '5px'}}>Брони:</h1>
            <br/>
            <div className="err-message">
                {errorMessage !== "" && (
                    <b>{errorMessage}</b>
                )}
            </div>
            <div>
                {FilteredBookings.length > 0 ? (
                    <div>
                        {FilteredBookings.map((booking: Booking) => (
                            <li key={booking.BookingId}>
                                <BookingCardToPage BookingId={booking.BookingId} RoomId={booking.RoomId} CheckIn={new Date(booking.CheckIn)} CheckOut={new Date(booking.CheckOut)} />
                            </li>
                        ))}
                    </div>
                ) : (
                    <div>
                        <p className="text">
                        У вас еще нет броней. Вы можете выбрать отель и забронировать номер.{' '}
                        <button className="btn-registration" onClick={() => navigate("/hotels")}>Перейти к отелям</button>
                        </p>
                    </div>
                )}
            </div>
        </div>
    );

}
export default BookingsPage;