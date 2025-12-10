import {FormEvent, useEffect, useState} from "react";
import {GetCurrentUser, updateUserName} from "../api/AppApi.ts";
import '../css/ProfilePage.css';

export function ProfilePage() {
    const [userName, setUserName] = useState("");
    const [email, setEmail] = useState("");

    const [name, setName] = useState("");

    const [errorMessage, setErrorMessage] = useState<string>("");

    const [proverka, setProverka] = useState(0);

    useEffect(() => {
        console.error("Update")
        GetCurrentUser(localStorage.getItem("token") ?? "").then((res) => {
            setUserName(res.Name);
            setEmail(res.Email);
        });
    }, [proverka]);


    const handleSubmit = (e: FormEvent) => {
        e.preventDefault();
        (async () => {
            try {
                if (!name) {
                    setErrorMessage("Введите новое имя");
                    return;
                }

                const response = await updateUserName({ name, email }, localStorage.getItem("token") ?? "");
                console.log(response);
                
                setErrorMessage('');
                setProverka(proverka + 1);
                alert("Данные обновлены");
            } catch (error: any) {
                if (error.name === "400") {
                    setErrorMessage(`Ошибка при обновлении профиля. Имя должно быть от 5 символов или пустым чтобы не обновлять.`);
                } else {
                    setErrorMessage(`Произошла ошибка: ${error.message}`);
                }
                setProverka(proverka + 1);
            }
        })();
    };


    return (
        <div className="profile-page">
            <div className="profile-info">
                <div className="profile-header">
                    <h1>Профиль</h1>
                    <h3>{email}</h3>
                    <br/>
                    <h3>{userName}</h3>
                </div>
            </div>
            <br />
            <form className="form" onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Имя:</label>
                    <input
                        type="text"
                        id="name"
                        placeholder="Ваше новое имя"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                    />
                </div>
                <button type="submit" className="update-button">
                    Обновить данные
                </button>
            </form>
            <br/>
            <div className="err-message">
                {errorMessage !== "" && (
                    <b>{errorMessage}</b>
                )}
            </div>
        </div>
    );

}
export default ProfilePage;