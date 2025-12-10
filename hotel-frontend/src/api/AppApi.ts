import axios from "axios";

const AUTH_API = import.meta.env.VITE_AUTH_API ?? "http://localhost:8000";
const BOOKING_API = import.meta.env.VITE_BOOKING_API ?? "http://localhost:8001";

const authApi = axios.create({
    baseURL: AUTH_API,
    headers: { "Content-Type": "application/json" },
});

const bookingApi = axios.create({
    baseURL: BOOKING_API,
    headers: { "Content-Type": "application/json" },
});

// Models (frontend shape kept for compatibility with existing components)
export interface User {
    UserId: string;
    Email: string;
    Name: string;
}

export interface Hotel {
    HotelId: string;
    Name: string;
    Location: string;
    Description: string;
    ImgUrl: string | null;
}

export interface Room {
    RoomId: string;
    HotelId: string;
    RoomNumber: string;
    RoomType: number;
    PricePerNight: number;
    ImgUrl: string | null;
}

export interface Booking {
    BookingId: string;
    UserId: string;
    RoomId: string;
    CheckIn: string;
    CheckOut: string;
}

export interface LoginResponse {
    token: string;
}

export interface RegistrationResponse {
    token: string;
}

// Mappers from backend snake_case to frontend shape
const mapUser = (u: any): User => ({
    UserId: u.id,
    Email: u.email,
    Name: u.name,

});

const mapHotel = (h: any): Hotel => ({
    HotelId: h.id,
    Name: h.name,
    Location: h.location,
    Description: h.description,
    ImgUrl: h.img_url ?? null,
});

const mapRoom = (r: any): Room => ({
    RoomId: r.id,
    HotelId: r.hotel_id,
    RoomNumber: r.room_number,
    RoomType: r.room_type,
    PricePerNight: Number(r.price_per_night),
    ImgUrl: r.img_url ?? null,
});

const mapBooking = (b: any): Booking => ({
    BookingId: b.id,
    UserId: b.user_id,
    RoomId: b.room_id,
    CheckIn: b.check_in_date,
    CheckOut: b.check_out_date,
});

// Helpers
const bearer = (token?: string) => {
    const t = (token && token.trim() !== "") ? token : (localStorage.getItem("token") ?? "");
    return t && t.trim() !== "" ? { Authorization: `Bearer ${t}` } : {};
};

// Authorization
export async function LoginUser(email: string, password: string) {
    const { data } = await authApi.post<{ access_token: string }>("/auth/login", {
        email,
        password,
    });
    return { token: data.access_token } as LoginResponse;
}

export async function RegistrationUser(name: string, email: string, password: string) {
    await authApi.post("/auth/register", { name, email, password });
    return LoginUser(email, password);
}

export async function GetCurrentUser(token?: string) {
    const { data } = await authApi.get("/auth/me", {
        headers: bearer(token),
    });
    return mapUser(data);
}

// Users
export const getUsers = async (token?: string) => {
    const { data } = await authApi.get("/users", { headers: bearer(token) });
    return (data as any[]).map(mapUser);
};

export const updateUserName = async (payload: { name: string; id?: string; email?: string }, token?: string) => {
    const { data } = await authApi.patch("/users", payload, { headers: bearer(token) });
    return mapUser(data);
};

export const deleteUser = async (userId: string, token?: string) => {
    await authApi.delete(`/users/${userId}`, { headers: bearer(token) });
};

// Hotels
export const getHotels = async () => {
    const { data } = await bookingApi.get("/hotels/");
    return (data as any[]).map(mapHotel);
};

export const CreateHotel = async (payload: {name: string, location: string, description: string, img_url: string}, token?: string) => {
    await bookingApi.post("/hotels/", payload, { headers: bearer(token) })
};

export const UpdateHotel = async (hotelId: string, payload: {name: string, location: string, description: string, img_url: string}, token?: string) => {
    await bookingApi.put(`/hotels/${hotelId}`, payload, { headers: bearer(token) })
};

export const deleteHotel = async (hotelId: string, token?: string) => {
    await bookingApi.delete(`/hotels/${hotelId}`, { headers: bearer(token) });
};

// Rooms
export const getRooms = async (hotelId: string) => {
    if (!hotelId) {
        return [];
    }
    const { data } = await bookingApi.get(`/hotels/${hotelId}/rooms`);
    return (data as any[]).map(mapRoom);
};

export const getRoomById = async (roomId: string) => {
    if (!roomId) {
        return null;
    }
    const { data } = await bookingApi.get(`/rooms/${roomId}`);
    return mapRoom(data);
};

export const CreateRoom = async (hotelId: string, payload: {room_number: string, room_type: number, price_per_night: number, img_url: string}, token?: string)=> {
    await bookingApi.post(`/hotels/${hotelId}/rooms`, payload, { headers: bearer(token) })
};

export const UpdateRoom = async (roomId: string, payload: {room_number: string, room_type: number, price_per_night: number, img_url: string}, token?: string) => {
    await bookingApi.put(`/rooms/${roomId}`, payload, { headers: bearer(token) })
};

export const DeleteRoom = async (roomId: string, token?: string) => {
    await bookingApi.delete(`/rooms/${roomId}`, {
        headers: bearer(token),
    });
};

// Bookings
export const getBookings = async (token?: string) => {
    const { data } = await bookingApi.get("/bookings/my", {
        headers: bearer(token),
    });
    return (data as any[]).map(mapBooking);
};

export const createBooking = async (
    payload: { room_id: string; check_in_date: string; check_out_date: string },
    token?: string
) => {
    const { data } = await bookingApi.post("/bookings/", payload, {
        headers: bearer(token),
    });
    return mapBooking(data);
};

export const DeleteBooking = async (bookingId: string, token?: string) => {
    await bookingApi.delete(`/bookings/${bookingId}`, {
        headers: bearer(token),
    });
};

