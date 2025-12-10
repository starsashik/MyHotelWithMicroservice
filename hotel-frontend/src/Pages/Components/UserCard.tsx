import React from 'react';
import Card from 'react-bootstrap/Card';

interface UserCardProps {
    email: string;
    name: string;
    Id: string;
}


const UserCard: React.FC<UserCardProps> = ({ email, name, Id}) => {
    return (
        <Card body>
            Id : {Id} 
            <br/>
            Почта : {email}
            <br/>
            Имя : {name}
        </Card>
    );
}

export default UserCard;