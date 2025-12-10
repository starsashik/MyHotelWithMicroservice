import React, {FormEvent, useEffect, useState} from "react";
import {createBooking, getRooms, Room} from "../api/AppApi.ts";
import '../css/RoomsPage.css';
import {useAppDispatch, useAppSelector} from "../redux/Hooks.tsx";
import {Button} from "react-bootstrap";
import RoomCardToPage from "./Components/RoomCardToPage.tsx";
import {setRoomId} from "../redux/HotelSlice.tsx";

export function BookingsPage() {
    const user = useAppSelector((state) => state.user);
    const hotel = useAppSelector((state) => state.hotel);
    const dispatch = useAppDispatch();

    const [FilteredRooms_1, setFilteredRooms_1] = useState<Room[]>([]);
    const [FilteredRooms_2, setFilteredRooms_2] = useState<Room[]>([]);
    const [FilteredRooms_3, setFilteredRooms_3] = useState<Room[]>([]);

    const [DateInToCreate, setDateInToCreate] = useState<Date>(new Date());
    const [DateOutToCreate, setDateOutToCreate] = useState<Date>(new Date());

    const [errorMessage, setErrorMessage] = useState<string>("");

    const loadRooms = async () => {
        try {
            if (!hotel.hotelId) {
                setErrorMessage("Сначала выберите отель");
                setFilteredRooms_1([]);
                setFilteredRooms_2([]);
                setFilteredRooms_3([]);
                return;
            }

            const rooms = await getRooms(hotel.hotelId);
            const forHotel = rooms.filter((r) => r.HotelId === hotel.hotelId);

            setFilteredRooms_1(forHotel.filter((r) => r.RoomType === 1));
            setFilteredRooms_2(forHotel.filter((r) => r.RoomType === 2));
            setFilteredRooms_3(forHotel.filter((r) => r.RoomType === 3));
            setErrorMessage("");
        } catch (error: any) {
            setErrorMessage(`Произошла ошибка: ${error.message ?? error}`);
        }
    };

    useEffect(() => {
        loadRooms();
    }, [hotel.hotelId]);

    const handleSubmit_createBooking = (e: FormEvent) => {
        e.preventDefault();
        (async () => {
            try {
                if (!hotel.roomId) {
                    setErrorMessage("Выберите комнату");
                    return;
                }

                await createBooking(
                    {
                        room_id: hotel.roomId,
                        check_in_date: formatDateForInput(DateInToCreate),
                        check_out_date: formatDateForInput(DateOutToCreate),
                    },
                    localStorage.getItem("token") ?? ""
                );
                alert("Вы забронировали номер!");
                setErrorMessage("");
                dispatch(setRoomId(""));
            } catch (error: any) {
                const detail = error?.response?.data?.detail[0].msg;
                if (detail) {
                    setErrorMessage(typeof detail === "string" ? detail : JSON.stringify(detail));
                } else {
                    setErrorMessage(`Произошла ошибка: ${error.message ?? error}`);
                }
            }
        })();
    };

    const handleDateChangeIn = (e: React.ChangeEvent<HTMLInputElement>) => {
        const newDate = new Date(e.target.value);
        if (!isNaN(newDate.getTime())) { // Проверяем, что дата валидная
            setDateInToCreate(newDate);
        }
    };

    const handleDateChangeOut = (e: React.ChangeEvent<HTMLInputElement>) => {
        const newDate = new Date(e.target.value);
        if (!isNaN(newDate.getTime())) { // Проверяем, что дата валидная
            setDateOutToCreate(newDate);
        }
    };

    const formatDateForInput = (date: Date): string => {
        return date.toISOString().split('T')[0]; // Например, "2025-05-20"
    };

    return (
        <div className="rooms-page">
            <h1 style={{display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '5px'}}>Бронирование номеров</h1>
            <br/>
            <div style={{display: 'flex', gap: '50px', alignItems: 'flex-start'}}>
                <div style={{flex: 1}}>
                    <h1>Обычные номера:</h1>
                    <div>
                            {FilteredRooms_1.length > 0 ? (
                                <div>
                                    {FilteredRooms_1.map((room: Room) => (
                                        <li key={room.RoomId}>
                                            <RoomCardToPage RoomId={room.RoomId} RoomNumber={room.RoomNumber} PricePerNight={room.PricePerNight} ImgUrl={room.ImgUrl} />
                                        </li>
                                    ))}
                                </div>
                            ) : (
                                <div>
                                    <p>Нет номеров.</p>
                                </div>
                            )}
                        </div>
                    <br/>
                    <h1>Люкс номера:</h1>
                    <div>
                        {FilteredRooms_2.length > 0 ? (
                            <div>
                                {FilteredRooms_2.map((room: Room) => (
                                    <li key={room.RoomId}>
                                        <RoomCardToPage RoomId={room.RoomId} RoomNumber={room.RoomNumber} PricePerNight={room.PricePerNight} ImgUrl={room.ImgUrl} />
                                    </li>
                                ))}
                            </div>
                        ) : (
                            <div>
                                <p>Нет номеров.</p>
                            </div>
                        )}
                    </div>
                    <br/>
                    <h1>Президентские номера:</h1>
                    <div>
                        {FilteredRooms_3.length > 0 ? (
                            <div>
                                {FilteredRooms_3.map((room: Room) => (
                                    <li key={room.RoomId}>
                                        <RoomCardToPage RoomId={room.RoomId} RoomNumber={room.RoomNumber} PricePerNight={room.PricePerNight} ImgUrl={room.ImgUrl} />
                                    </li>
                                ))}
                            </div>
                        ) : (
                            <div>
                                <p>Нет номеров.</p>
                            </div>
                        )}
                    </div>
                </div>
                <div style={{flex: 0.5}}>
                    {hotel.roomId != "" && user.userId != "" ? (
                        <div>
                            <h4>Создание брони</h4>
                            <form className="form" onSubmit={handleSubmit_createBooking}>
                                <div className="form-group">
                                    <label>
                                        Дата въезда
                                    </label>
                                    <input
                                        type="date"
                                        placeholder="Дата"
                                        value={formatDateForInput(DateInToCreate)}
                                        onChange={handleDateChangeIn}
                                        required
                                    />
                                </div>
                                <div className="form-group">
                                    <label>
                                        Дата выезда
                                    </label>
                                    <input
                                        type="date"
                                        placeholder="Дата"
                                        value={formatDateForInput(DateOutToCreate)}
                                        onChange={handleDateChangeOut}
                                        required
                                    />
                                </div>
                                <Button type="submit" className="update-button">
                                    Создать бронь
                                </Button>
                            </form>
                        </div>
                    ) : (
                        <div>
                            <p>Выберите комнату</p>
                        </div>
                    )}
                    <div className="err-message">
                        {errorMessage !== "" && (
                            <b>{errorMessage}</b>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );

}

export default BookingsPage;