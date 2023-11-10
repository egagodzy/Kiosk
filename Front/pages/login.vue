<template>
    <div class="flex bg-slate-700 w-full h-screen pb-[40px]">
        <form class="flex flex-col mx-auto my-auto w-5/6 h-5/6 bg-orange-500" @submit.prevent="Login">
            <div class="flex w-full flex-col mx-auto my-auto">
                <input v-model="LoginForm.username" class="flex w-5/6 mx-auto text-center" type="text" placeholder="Имя пользователя">
                <p v-if="Error_Input_Username" class="flex mx-auto mt-2 text-red-700">{{ Error_Input_Username }}</p>
                <input v-model="LoginForm.userpassword" class="flex w-5/6 mx-auto mt-10 text-center" type="password" placeholder="Пароль">
                <p v-if="Error_Input_Passowrd" class="flex mx-auto mt-2 text-red-700">{{ Error_Input_Passowrd }}</p>
                <button class="bg-green-500 w-1/6 mx-auto hover:bg-green-700 text-white font-bold mt-5 py-2 px-2 rounded" type="submit">Войти</button>
            </div>
        </form>
    </div>
</template>

<script>
import axios from 'axios';
    export default {
        data() {
            return {
                LoginForm: {
                    username: '',
                    userpassword: ''
                },
                Error_Input_Username: '',
                Error_Input_Passowrd: '',
            }
        },
        methods: {
            async Login() {
                if (this.LoginForm.username === '' && this.LoginForm.userpassword === '') {
                    this.Error_Input_Username = '';
                    this.Error_Input_Passowrd = '';
                    this.Error_Input_Username = 'Имя пользователя не должно быть пустым.';
                    this.Error_Input_Passowrd = 'Пароль не должен быть пустым.';
                } else if (this.LoginForm.username === '') {
                    this.Error_Input_Username = '';
                    this.Error_Input_Passowrd = '';
                    this.Error_Input_Username = 'Имя пользователя не должно быть пустым.';
                } else if (this.LoginForm.userpassword === '') {
                    this.Error_Input_Username = '';
                    this.Error_Input_Passowrd = '';
                    this.Error_Input_Passowrd = 'Пароль не должен быть пустым.';
                } else {
                    console.log(this.LoginForm);
                    axios.post("http://localhost:1337/login/", this.LoginForm)
                    .then(response => {
                        console.log(response.data.Auth);
                        if (response.data.Auth === 1) {
                            this.Error_Input_Username = '';
                            this.Error_Input_Passowrd = '';
                            this.Error_Input_Username = 'Неверное имя пользователя';
                        } else if (response.data.Auth === 2) {
                            this.Error_Input_Username = '';
                            this.Error_Input_Passowrd = '';
                            this.Error_Input_Username = 'Неверный пароль';
                        } else {
                            if (process.client) {
                                localStorage.setItem("token", response.data.Auth);
                                navigateTo("/controlpanel");
                            }
                        }
                    })
                    .catch(error => console.log(error))
                }
            }
        }
    }
</script>