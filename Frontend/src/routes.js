import { createWebHistory, createRouter } from 'vue-router';


import home from './components/home.vue';
import Login from './components/Login.vue';
import Register from './components/Register.vue';
import Dashboard from './components/Dashboard.vue';



const routes = [
    { path: "/" , component: home},
    {path: "/login",component: Login},
    {path:"/register",component: Register},
    {path:"/dashboard",component: Dashboard},
//     {path:"/user",components:[
//         {path: "search", component: UserSearch},
//         {path: "bookings/:spotid", component: UserBookings},
//         {path:"update_booking/:spotid",component: UserUpdateBooking},
//         {path:"cancel_booking/:spotid",component: UserCancelBooking},
//         {path:"release_booking/:spotid",component: UserReleaseBooking},
//     ],
// component: User},
//    {path: "/admin", components:[
//     {path:"create_lot", component: AdminCreateLot},
//     {path:"update_lot/:lotid", component: AdminUpdateLot},
//     {path:"delete_lot/:lotid", component: AdminDeleteLot},
//     {path:"view_spot/:spotid", component: AdminViewSpots},
//     {path:"delete_spot/:spotid", component: AdminDeleteSpot},
//     {path:"user_search",component: AdminUserSearch},
//     {path:"lot_search",components: AdminLotSearch}
//    ]}


]


export const router =createRouter({
    history: createWebHistory(),
    routes
})
