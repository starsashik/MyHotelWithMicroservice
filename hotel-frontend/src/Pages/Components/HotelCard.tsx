import React from 'react';
import Card from 'react-bootstrap/Card';

interface HotelCardProps {
    HotelId : string;
    Name : string;
    Location : string;
    Description: string;
    ImgUrl : string;
}


const HotelCard: React.FC<HotelCardProps> = ({ HotelId, Name, Location, Description, ImgUrl }) => {
    return (
        <Card body>
            <img
            src={ImgUrl ?? ""}
            alt="Image"
            style={{ width: '160px', height: '90px' }} // Размер можно изменить
            />
            <br/>
            {HotelId}
            <br/>
            Название : {Name}
            <br/>
            Локация : {Location}
            <br/>
            Описание : {Description}
        </Card>
    );
}

export default HotelCard;