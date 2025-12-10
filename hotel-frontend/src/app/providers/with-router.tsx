import { BrowserRouter } from 'react-router-dom';
import { IWithProviderProps } from './types';

export const WithRouter: React.FC<IWithProviderProps> = ({ children }) => {
    return (
        <BrowserRouter>
            {children}
        </BrowserRouter>
    );
};
