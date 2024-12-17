import { createApp } from "vue"
import { createRouter, createWebHistory } from "vue-router"
import axios from "axios"
import App from "./App.vue"
import LoginPage from "./pages/login-page.vue"

axios.defaults.withCredentials = true
const app = createApp(App)
const routes = [
	{ path: "/login", name: "Login", component: LoginPage },
]

const router = createRouter({
	history: createWebHistory(),
	routes,
})

router.beforeEach(async (to, from, next) => {
	const { logged_in } = await checkUserStatus()

	if (to.path === "/login" && logged_in) {
		next("/")
	} else if (!logged_in && to.path !== "/login") {
		next("/login")
	} else {
		next()
	}
})

async function checkUserStatus() {
	try {
		const response = await axios.get("/api/user/status")
		return { logged_in: response.data.logged_in }
	} catch (error) {
		return { logged_in: false }
	}
}

app.use(router)
app.mount("#app")
