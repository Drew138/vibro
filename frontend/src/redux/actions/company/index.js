import axios from "axios"
import { POST_COMPANY_ENDPOINT, 
        PATCH_COMPANY_ENDPOINT } from "../../../../config"

export const editCompany = () => {
    return dispatch => {
        try {
            const res = await axios.patch(PATCH_COMPANY_ENDPOINT)
        } catch (e) {

        }
    }
}

export const createCompany = () => {
    return dispatch => {
        try {
            const res = await axios.post(POST_COMPANY_ENDPOINT)


        } catch (e) {

        }
    }
}