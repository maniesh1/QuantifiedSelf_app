import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignUp from '@/components/SignUp'
import Errors from '@/components/Errors'
import Home from '@/components/Home'
import Login from '@/components/Login'
import Logout from '@/components/Logout'
import About from '@/components/About'
import AddTracker from '@/components/AddTracker'
import UpdateTracker from '@/components/UpdateTracker'
import Logs from '@/components/Logs'
import UpdateLog from '@/components/UpdateLog'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUp
  },
  {
    path: '/errors',
    name: 'errors',
    component: Errors
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/add-tracker',
    name: 'add-tracker',
    component: AddTracker
  },
  {
    path: '/update-tracker/:id',
    name: 'update-tracker',
    component: UpdateTracker
  },
  {
    path: '/update-log/:id',
    name: 'update-log',
    component: UpdateLog
  },
  {
    path: '/logs/:name',
    name: 'logs',
    component: Logs
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: About
  }
]

const router = new VueRouter({
  routes
})

export default router
