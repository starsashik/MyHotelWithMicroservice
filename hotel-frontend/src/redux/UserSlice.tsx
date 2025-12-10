import {createSlice, type PayloadAction} from '@reduxjs/toolkit'

export interface UserState {
    isLoggedIn: boolean;
    email: string;
    userId: string;
    update: number;
}

const initialState: UserState = {
    isLoggedIn: false,
    email: "",
    userId: "",
    update: 0
}

export const userSlice = createSlice({
    name: 'user',
    initialState,
    reducers: {
        setIsLoggedIn: (state, action: PayloadAction<boolean>) => {
            state.isLoggedIn = action.payload;
        },
        setEmail: (state, action: PayloadAction<string>) => {
            state.email = action.payload;
        },
        setUserId: (state, action: PayloadAction<string>) => {
            state.userId = action.payload;
        },
        setUpdate: (state) => {
            state.update = state.update + 1;
        },
    }
})

export const {setIsLoggedIn, setEmail, setUserId, setUpdate} = userSlice.actions