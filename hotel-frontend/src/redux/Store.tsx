import {configureStore} from "@reduxjs/toolkit";
import {userSlice} from "./UserSlice.tsx";
import {hotelSlice} from "./HotelSlice.tsx";

export const store = configureStore({
    reducer: {
        user: userSlice.reducer,
        hotel: hotelSlice.reducer
    },
});

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch