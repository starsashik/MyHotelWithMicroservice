import {setHotelId, setNumberBookings} from "../../redux/HotelSlice.tsx";

;import React from 'react';
import Card from 'react-bootstrap/Card';
import { DeleteBooking, getRoomById, Room, Hotel, getHotels} from "../../api/AppApi.ts";
import {useAppDispatch, useAppSelector} from "../../redux/Hooks.tsx";
import {useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";

interface BookingCardToPageProps {
    BookingId : string;
    RoomId: string;
    CheckIn: Date;
    CheckOut: Date;
}


const BookingCardToPage: React.FC<BookingCardToPageProps> = ({ BookingId, RoomId, CheckIn, CheckOut }) => {
    const hotel = useAppSelector((state)=>state.hotel);
    const dispatch = useAppDispatch();
    const navigate = useNavigate();
    const [selectedRoom, setSelectedRoom] = useState<Room | null>(null);
    const typeRoom = ["Обычный", "Люкс", "Президентский"]
    const [hotels, setHotels] = useState<Hotel | null>(null);

    useEffect(() => {
        (async () => {
            const room = await getRoomById(RoomId);
            setSelectedRoom(room);
            if (room) {
                const data_3 = await getHotels();
                const foundHotel = data_3.find((r) => r.HotelId === room.HotelId);
                if (foundHotel) {
                    setHotels(foundHotel);
                }
            }
        })();
    }, [RoomId]);


    const handleGoToRoom = () => {
        if (selectedRoom) {
            dispatch(setHotelId(selectedRoom.HotelId));
            navigate("/rooms");
        }
        else{
            navigate("/hotels");
        }

    }

    const handleDelete = () => {
        (async () => {
            console.log(hotel.numberBookings);
            await DeleteBooking(BookingId, localStorage.getItem("token") ?? "");
            alert("Бронь удалена!");
            dispatch(setNumberBookings());
            navigate("/bookings");
        })();
    }


    return (
        <Card body>
            <div style={{ display: 'flex', gap: '20px', alignItems: 'flex-start' }}>
                <div style={{ flex: 1 }}>
                    Номер комнаты : {selectedRoom ? selectedRoom.RoomNumber.toString() : ""}
                    <br/>
                    Тип комнаты : {selectedRoom ? typeRoom[selectedRoom.RoomType - 1] : ""}
                    <br/>
                    Цена за одну ночь : {selectedRoom ? selectedRoom.PricePerNight.toString() : ""}
                    <br/>
                    Дата заезда : {CheckIn.toString()}
                    <br/>
                    Дата выезда : {CheckOut.toString()}
                    <br/>
                    Отель : {hotels?.Name ?? ""}
                    <br/>
                </div>
                <div>
                    {selectedRoom ? <img
                        src={selectedRoom.ImgUrl ?? ""}
                        alt="Image"
                        style={{ width: '320px', height: '180px', }} // Размер можно изменить
                    /> : "Нет картинки"}
                </div>
            </div>
            <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
                <button className="update-button" onClick={handleGoToRoom}>Перейти к отелю</button>
                <button className="delete-button" onClick={handleDelete}>Удалить бронь</button>
            </div>
        </Card>
    );
}

export default BookingCardToPage;