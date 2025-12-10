import React from 'react';
import Card from 'react-bootstrap/Card';

interface RoomCardProps {
    RoomId : string;
    RoomNumber : string;
    RoomType : number;
    PricePerNight : number;
    ImgUrl : string;
}


const RoomCard: React.FC<RoomCardProps> = ({ RoomId, RoomNumber, RoomType, PricePerNight, ImgUrl }) => {
    return (
        <Card body>
            <img
            src={ImgUrl ?? ""}
            alt="Image"
            style={{ width: '160px', height: '90px' }} // Размер можно изменить
            />
            <br/>
            Id : {RoomId}
            <br/>
            Номер комнаты : {RoomNumber}
            <br/>
            Тип комнаты : {RoomType}
            <br/>
            Цена за одну ночь : {PricePerNight}
        </Card>
    );
}

export default RoomCard;