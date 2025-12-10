import {FormEvent, useEffect, useState} from "react";
import {
    getUsers,
    Hotel,
    User,
    Room,
    getHotels,
    deleteUser,
    CreateHotel,
    UpdateHotel,
    deleteHotel,
    getRooms,
    CreateRoom,
    UpdateRoom,
    DeleteRoom
} from "../api/AppApi.ts";
import UserCard from "./Components/UserCard.tsx";
import {Button} from "react-bootstrap";
import "../css/AdminPage.css"
import HotelCard from "./Components/HotelCard.tsx";
import RoomCard from "./Components/RoomCard.tsx";

export function AdminPage() {
    // Users
    const [showUsers, setShowUsers] = useState(false);
    const [showDeleteUser, setShowDeleteUser] = useState(false);

    // Hotels
    const [showHotels, setShowHotels] = useState(false);
    const [showCreateHotels, setShowCreateHotels] = useState(false);
    const [showUpdateHotels, setShowUpdateHotels] = useState(false);
    const [showDeleteHotels, setShowDeleteHotels] = useState(false);

    // Rooms
    const [showRooms, setShowRooms] = useState(false);
    const [showCreateRooms, setShowCreateRooms] = useState(false);
    const [showUpdateRooms, setShowUpdateRooms] = useState(false);
    const [showDeleteRooms, setShowDeleteRooms] = useState(false);


    // list models
    const [Users, setUsers] = useState<User[]>([]);
    const [Hotels, setHotels] = useState<Hotel[]>([]);
    const [Rooms, setRooms] = useState<Room[]>([]);

    // Users
    const [UserIdDel, setUserIdDel] = useState('');

    // Hotels
    const [HotelName, setHotelName] = useState('');
    const [HotelLocation, setHotelLocation] = useState('');
    const [HotelDescription, setHotelDescription] = useState('');
    const [HotelImage, setHotelImage] = useState('');

    const [HotelIdDel, setHotelIdDel] = useState('');

    const [HotelIdUpdate, setHotelIdUpdate] = useState('');
    const [NewHotelName, setNewHotelName] = useState('');
    const [NewHotelLocation, setNewHotelLocation] = useState('');
    const [NewHotelDescription, setNewHotelDescription] = useState('');
    const [NewHotelImage, setNewHotelImage] = useState('');

    // Rooms
    const [HotelIdToFilter, setHotelIdToFilter] = useState('');
    const [HotelIdToCreateRoom, setHotelIdToCreateRoom] = useState('');
    const [RoomNumber, setRoomNumber] = useState('');
    const [RoomType, setRoomType] = useState<number>(0);
    const [PricePerNight, setPricePerNight] = useState<number>(0);
    const [ImageRoom, setImageRoom] = useState('');

    const [RoomIdDel, setRoomIdDel] = useState('');

    const [RoomIdUpdate, setRoomIdUpdate] = useState('');
    const [NewRoomNumber, setNewRoomNumber] = useState('');
    const [NewRoomType, setNewRoomType] = useState<number>(0);
    const [NewPricePerNight, setNewPricePerNight] = useState<number>(0);
    const [NewImageRoom, setNewImageRoom] = useState('');

    // Dop
    const [errorMessage, setErrorMessage] = useState<string>("");
    const [UpdatePage, setUpdatePage] = useState(false);

    /*_____________________________________________________________*/

    useEffect(() => {
        (async () => {
            const data = await getUsers();
            setUsers(data);
            console.log(data)
        })();
    }, [showUsers, UpdatePage]);


    useEffect(() => {
        (async () => {
            const data_3 = await getHotels();
            setHotels(data_3);
            console.log(data_3);
        })();
    }, [showHotels, UpdatePage]);

    useEffect(() => {
        (async () => {
            try {
                const data_4 = await getRooms(HotelIdToFilter);
                setRooms(data_4);
                console.log(data_4);

                setErrorMessage('');
            } catch (error: any) {
                if (error.response?.status === 401) {
                    setErrorMessage('Неверный токен');
                } else {
                    setErrorMessage(`Произошла ошибка: ${error.message}`);
                }
                setRooms([]);
            }
        })();
    }, [showRooms, UpdatePage]);


    // Users
    const handleSubmit_deleteUser = (e: FormEvent) => {
        e.preventDefault();
        (async () => {
            try {
                await deleteUser(UserIdDel, localStorage.getItem("token") ?? "");

                setErrorMessage('');
                setUpdatePage(!UpdatePage);
            } catch (error: any) {
                if (error.response?.status === 401) {
                    setErrorMessage('Неверный токен');
                } else {
                    setErrorMessage(`Произошла ошибка: ${error.message}`);
                }
            }
        })();
    };

    // Hotel
    const handleSubmit_createHotel = (e: FormEvent) => {
        e.preventDefault();
        (async () => {
            try {
                await CreateHotel({
                    name: HotelName,
                    location: HotelLocation,
                    description: HotelDescription,
                    img_url: HotelImage || ""
                }, localStorage.getItem("token") ?? "");

                setErrorMessage('');
                setUpdatePage(!UpdatePage);
            } catch (error: any) {
                if (error.response?.status === 401 || error.response?.status === 400) {
                    setErrorMessage('Неверные данные.');
                } else {
                    setErrorMessage(`Произошла ошибка: ${error.message}`);
                }
            }
        })();
    };

    const handleSubmit_updateHotel = (e: FormEvent) => {
        e.preventDefault();
        (async () => {
            try {
                await UpdateHotel(HotelIdUpdate, {
                        name: NewHotelName,
                        location: NewHotelLocation,
                        description: NewHotelDescription,
                        img_url: NewHotelImage || ""
                    }, localStorage.getItem("token") ?? "");

                setErrorMessage('');
                setUpdatePage(!UpdatePage);
            } catch (error: any) {
                if (error.response?.status === 401 || error.response?.status === 400) {
                    setErrorMessage('Неверные данные.');
                } else {
                    setErrorMessage(`Произошла ошибка: ${error.message}`);
                }
            }
        })();
    };

    const handleSubmit_deleteHotel = (e: FormEvent) => {
        e.preventDefault();
        (async () => {
            try {
                await deleteHotel(HotelIdDel, localStorage.getItem("token") ?? "");

                setErrorMessage('');
                setUpdatePage(!UpdatePage);
            } catch (error: any) {
                if (error.response?.status === 401) {
                    setErrorMessage('Неверный токен');
                } else {
                    setErrorMessage(`Произошла ошибка: ${error.message}`);
                }
            }
        })();
    };

    // Room
    const handleSubmit_createRoom = (e: FormEvent) => {
        e.preventDefault();
        (async () => {
            try {
                await CreateRoom(HotelIdToCreateRoom, {
                    room_number: RoomNumber, 
                    room_type: RoomType, 
                    price_per_night: PricePerNight, 
                    img_url: ImageRoom
                }, localStorage.getItem("token") ?? "");

                setErrorMessage('');
                setUpdatePage(!UpdatePage);
            } catch (error: any) {
                if (error.response?.status === 401 || error.response?.status === 400) {
                    setErrorMessage('Неверные данные.');
                } else {
                    setErrorMessage(`Произошла ошибка: ${error.message}`);
                }
            }
        })();
    };

    const handleSubmit_updateRoom = (e: FormEvent) => {
        e.preventDefault();
        (async () => {
            try {
                await UpdateRoom(RoomIdUpdate, {
                    room_number: NewRoomNumber, 
                    room_type: NewRoomType, 
                    price_per_night: NewPricePerNight, 
                    img_url: NewImageRoom
                }, localStorage.getItem("token") ?? "");

                setErrorMessage('');
                setUpdatePage(!UpdatePage);
            } catch (error: any) {
                if (error.response?.status === 401 || error.response?.status === 400) {
                    setErrorMessage('Неверные данные.');
                } else {
                    setErrorMessage(`Произошла ошибка: ${error.message}`);
                }
            }
        })();
    };

    const handleSubmit_deleteRoom = (e: FormEvent) => {
        e.preventDefault();
        (async () => {
            try {
                await DeleteRoom(RoomIdDel, localStorage.getItem("token") ?? "");

                setErrorMessage('');
                setUpdatePage(!UpdatePage);
            } catch (error: any) {
                if (error.response?.status === 401) {
                    setErrorMessage('Неверный токен');
                } else {
                    setErrorMessage(`Произошла ошибка: ${error.message}`);
                }
            }
        })();
    };

    /*_____________________________________________________________*/

    return (
        <div className="admin-page">
            <h1 style={{display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '5px'}}>Панель администратора</h1>
            <br/>
            <div className="err-message">
                {errorMessage !== "" && (
                    <b>{errorMessage}</b>
                )}
            </div>
            <div>
                <h1>Пользователи</h1>
                <div style={{display: 'flex', alignItems: 'left', justifyContent: 'left', gap: '20px'}}>
                    <label>
                        <input
                            type="checkbox"
                            checked={showUsers}
                            onChange={() => setShowUsers(!showUsers)}
                        />
                        Показывать пользователей
                    </label>
                </div>
                {showUsers &&
                    <div>
                        {Users.length > 0 ? (
                            <div>
                                {Users.map((user: User) => (
                                    <li key={user.Email}>
                                        <UserCard email={user.Email} name={user.Name} Id={user.UserId}/>
                                    </li>
                                ))}
                            </div>
                        ) : (
                            <div>
                                <p>Нет пользователей.</p>
                            </div>
                        )}
                    </div>
                }
                <br/>
                <label>
                    <input
                        type="checkbox"
                        checked={showDeleteUser}
                        onChange={() => setShowDeleteUser(!showDeleteUser)}
                    />
                    Показывать удаление пользователей
                </label>
                {showDeleteUser &&
                    <div>
                        <br/>
                        <h4>Удаление пользователя</h4>
                        <form className="form" onSubmit={handleSubmit_deleteUser}>
                            <div className="form-group">
                                <label>
                                    Guid пользователя
                                </label>
                                <input
                                    type="text"
                                    placeholder="Guid пользователся"
                                    value={UserIdDel}
                                    onChange={(e) => setUserIdDel(e.target.value)}
                                    required
                                />
                            </div>
                            <Button type="submit" className="update-button">
                                Удалить пользователя
                            </Button>
                        </form>
                    </div>
                }
            </div>
            <br/>
            <div>
                <h1>Отели</h1>
                <label>
                    <input
                        type="checkbox"
                        checked={showHotels}
                        onChange={() => setShowHotels(!showHotels)}
                    />
                    Показывать отели
                </label>
                <br/>
                {showHotels &&
                    <div>
                        {Hotels.length > 0 ? (
                            <div>
                                {Hotels.map((hotel: Hotel) => (
                                    <li key={hotel.HotelId}>
                                        <HotelCard HotelId={hotel.HotelId} Name={hotel.Name} Location={hotel.Location} Description={hotel.Description} ImgUrl={hotel.ImgUrl ?? ""}/>
                                    </li>
                                ))}
                            </div>
                        ) : (
                            <div>
                                <p>Нет Отелей.</p>
                            </div>
                        )}
                    </div>
                }
                <br/>
                <label>
                    <input
                        type="checkbox"
                        checked={showCreateHotels}
                        onChange={() => setShowCreateHotels(!showCreateHotels)}
                    />
                    Показывать создание отеля
                </label>
                {showCreateHotels &&
                    <div>
                        <br/>
                        <h4>Создание отеля</h4>
                        <form className="form" onSubmit={handleSubmit_createHotel}>
                            <div className="form-group">
                                <label>
                                    Название отеля
                                </label>
                                <input
                                    
                                    type="text"
                                    placeholder="Название отеля"
                                    value={HotelName}
                                    onChange={(e) => setHotelName(e.target.value)}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>
                                    Местоположение отеля
                                </label>
                                <input
                                    
                                    type="text"
                                    placeholder="Местоположение отеля"
                                    value={HotelLocation}
                                    onChange={(e) => setHotelLocation(e.target.value)}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>
                                    Описание отеля
                                </label>
                                <input
                                    
                                    type="text"
                                    placeholder="Описание отеля"
                                    value={HotelDescription}
                                    onChange={(e) => setHotelDescription(e.target.value)}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>
                                    Ссылка на картинку
                                </label>
                                <input
                                    type="text"
                                    placeholder="Ссылка на картинку в интернете"
                                    value={HotelImage}
                                    onChange={(e) => setHotelImage(e.target.value)}
                                    required
                                />
                            </div>
                            <Button type="submit" className="update-button">
                                Создать Отель
                            </Button>
                        </form>
                    </div>
                }
                <br/>
                <br/>
                <label>
                    <input
                        type="checkbox"
                        checked={showUpdateHotels}
                        onChange={() => setShowUpdateHotels(!showUpdateHotels)}
                    />
                    Показывать обновление отеля
                </label>
                {showUpdateHotels &&
                    <div>
                        <br/>
                        <h4>Обновление отеля</h4>
                        <form className="form" onSubmit={handleSubmit_updateHotel}>
                            <div className="form-group">
                                <label>
                                    Guid отеля, который надо обновить
                                </label>
                                <input
                                    type="text"
                                    placeholder="Guid отеля"
                                    value={HotelIdUpdate}
                                    onChange={(e) => setHotelIdUpdate(e.target.value)}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>
                                    Новое название отеля
                                </label>
                                <input

                                    type="text"
                                    placeholder="Название отеля"
                                    value={NewHotelName}
                                    onChange={(e) => setNewHotelName(e.target.value)}
                                />
                            </div>
                            <div className="form-group">
                                <label>
                                    Новое местоположение отеля
                                </label>
                                <input

                                    type="text"
                                    placeholder="Местоположение отеля"
                                    value={NewHotelLocation}
                                    onChange={(e) => setNewHotelLocation(e.target.value)}
                                />
                            </div>
                            <div className="form-group">
                                <label>
                                    Новое описание отеля
                                </label>
                                <input

                                    type="text"
                                    placeholder="Описание отеля"
                                    value={NewHotelDescription}
                                    onChange={(e) => setNewHotelDescription(e.target.value)}
                                />
                            </div>
                            <div className="form-group">
                                <label>
                                    Ссылка на картинку
                                </label>
                                <input
                                    type="text"
                                    placeholder="Ссылка на картинку в интернете"
                                    value={NewHotelImage}
                                    onChange={(e) => setNewHotelImage(e.target.value)}
                                    required
                                />
                            </div>
                            <Button type="submit" className="update-button">
                                Обновить отель
                            </Button>
                        </form>
                    </div>
                }
                <br/>
                <br/>
                <label>
                    <input
                        type="checkbox"
                        checked={showDeleteHotels}
                        onChange={() => setShowDeleteHotels(!showDeleteHotels)}
                    />
                    Показывать удаление отеля
                </label>
                {showDeleteHotels &&
                    <div>
                        <br/>
                        <h4>Удаление отеля</h4>
                        <form className="form" onSubmit={handleSubmit_deleteHotel}>
                            <div className="form-group">
                                <label>
                                    Guid отеля
                                </label>
                                <input
                                    type="text"
                                    placeholder="Guid отеля"
                                    value={HotelIdDel}
                                    onChange={(e) => setHotelIdDel(e.target.value)}
                                    required
                                />
                            </div>
                            <Button type="submit" className="update-button">
                                Удалить отель
                            </Button>
                        </form>
                    </div>
                }
            </div>
            <br/>
            <div>
                <h1>Комнаты</h1>
                <form className="form">
                    <div className="form-group">
                        <label>
                            Guid отеля в котором ищем комнаты
                        </label>
                        <input
                            type="text"
                            placeholder="Guid отеля"
                            value={HotelIdToFilter}
                            onChange={(e) => setHotelIdToFilter(e.target.value)}
                            required
                        />
                    </div>
                </form>
                <label>
                    <input
                        type="checkbox"
                        checked={showRooms}
                        onChange={() => setShowRooms(!showRooms)}
                    />
                    Показывать номера в отелях
                </label>
                <br/>
                {showRooms &&
                    <div>
                        {Rooms.length > 0 ? (
                            <div>
                                {Rooms.map((room: Room) => (
                                    <li key={room.RoomId}>
                                        <RoomCard RoomId={room.RoomId} RoomNumber={room.RoomNumber} RoomType={room.RoomType} PricePerNight={room.PricePerNight} ImgUrl={room.ImgUrl ?? ""} />
                                    </li>
                                ))}
                            </div>
                        ) : (
                            <div>
                                <p>Нет комнат.</p>
                            </div>
                        )}
                    </div>
                }
                <br/>
                <label>
                    <input
                        type="checkbox"
                        checked={showCreateRooms}
                        onChange={() => setShowCreateRooms(!showCreateRooms)}
                    />
                    Показывать создание комнаты
                </label>
                {showCreateRooms &&
                    <div>
                        <br/>
                        <h4>Создание комнаты</h4>
                        <form className="form" onSubmit={handleSubmit_createRoom}>
                            <div className="form-group">
                                <label>
                                    Guid отеля
                                </label>
                                <input
                                    type="text"
                                    placeholder="Guid отеля"
                                    value={HotelIdToCreateRoom}
                                    onChange={(e) => setHotelIdToCreateRoom(e.target.value)}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>
                                    Номер комнаты
                                </label>
                                <input
                                    type="number"
                                    placeholder="Число от 1 до 1000"
                                    min="1" max="1000" step="1"
                                    value={RoomNumber}
                                    onChange={(e) => setRoomNumber((e.target.value))}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>
                                    Тип комнаты
                                </label>
                                <input
                                    type="number"
                                    placeholder="1 : Обычная, 2 : Люкс, 3 : Президентский"
                                    min="1" max="3" step="1"
                                    value={RoomType}
                                    onChange={(e) => setRoomType(parseInt(e.target.value) || 0)}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>
                                    Цена за ночь
                                </label>
                                <input
                                    type="number"
                                    placeholder="Число от 1 до 10000"
                                    min="1" max="10000" step="1"
                                    value={PricePerNight}
                                    onChange={(e) => setPricePerNight(parseInt(e.target.value) || 0)}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>
                                    Ссылка на картинку
                                </label>
                                <input
                                    type="text"
                                    placeholder="Ссылка на картинку в интернете"
                                    value={ImageRoom}
                                    onChange={(e) => setImageRoom(e.target.value)}
                                    required
                                />
                            </div>
                            <Button type="submit" className="update-button">
                                Создать комнату
                            </Button>
                        </form>
                    </div>
                }
                <br/>
                <br/>
                <label>
                    <input
                        type="checkbox"
                        checked={showUpdateRooms}
                        onChange={() => setShowUpdateRooms(!showUpdateRooms)}
                    />
                    Показывать обновление номера
                </label>
                {showUpdateRooms &&
                    <div>
                        <br/>
                        <h4>Обновление номера</h4>
                        <form className="form" onSubmit={handleSubmit_updateRoom}>
                            <div className="form-group">
                                <label>
                                    Guid номера, который надо обновить
                                </label>
                                <input
                                    type="text"
                                    placeholder="Guid номера"
                                    value={RoomIdUpdate}
                                    onChange={(e) => setRoomIdUpdate(e.target.value)}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>
                                    Новый номер комнаты
                                </label>
                                <input
                                    type="number"
                                    placeholder="Число от 1 до 1000"
                                    min="0" max="1000" step="1"
                                    value={NewRoomNumber}
                                    onChange={(e) => setNewRoomNumber(e.target.value)}
                                />
                            </div>
                            <div className="form-group">
                                <label>
                                    Новый тип комнаты
                                </label>
                                <input
                                    type="number"
                                    placeholder="1 : Обычная, 2 : Люкс, 3 : Президентский"
                                    min="0" max="3" step="1"
                                    value={NewRoomType}
                                    onChange={(e) => setNewRoomType(parseInt(e.target.value) || 0)}
                                />
                            </div>
                            <div className="form-group">
                                <label>
                                    Новая цена за ночь
                                </label>
                                <input
                                    type="number"
                                    placeholder="Число от 1 до 10000"
                                    min="0" max="10000" step="1"
                                    value={NewPricePerNight}
                                    onChange={(e) => setNewPricePerNight(parseInt(e.target.value) || 0)}
                                />
                            </div>
                            <div className="form-group">
                                <label>
                                    Ссылка на картинку
                                </label>
                                <input
                                    type="text"
                                    placeholder="Ссылка на картинку в интернете"
                                    value={NewImageRoom}
                                    onChange={(e) => setNewImageRoom(e.target.value)}
                                    required
                                />
                            </div>
                            <Button type="submit" className="update-button">
                                Обновить номеру
                            </Button>
                        </form>
                    </div>
                }
                <br/>
                <br/>
                <label>
                    <input
                        type="checkbox"
                        checked={showDeleteRooms}
                        onChange={() => setShowDeleteRooms(!showDeleteRooms)}
                    />
                    Показывать удаление номера
                </label>
                {showDeleteRooms &&
                    <div>
                        <br/>
                        <h4>Удаление номера</h4>
                        <form className="form" onSubmit={handleSubmit_deleteRoom}>
                            <div className="form-group">
                                <label>
                                    Guid номера
                                </label>
                                <input
                                    type="text"
                                    placeholder="Guid номера"
                                    value={RoomIdDel}
                                    onChange={(e) => setRoomIdDel(e.target.value)}
                                    required
                                />
                            </div>
                            <Button type="submit" className="update-button">
                                Удалить номер
                            </Button>
                        </form>
                    </div>
                }
            </div>
        </div>
    );
};

export default AdminPage;