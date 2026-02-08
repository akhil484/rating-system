import {useState, useEffect} from "react";
import axios from 'axios';
import { useParams } from "react-router-dom";
import './style.css'

function PostReview(){
    const [comment, setComment] = useState('');
    const [rating, setRating] = useState(3);

    const { uid } = useParams();

     const handleSubmit = async (e) => {
         e.preventDefault();

         const payload = {
             product_uid: uid,
             rating: Number(rating),
             comment: comment,
         };
        try{
            const response = await axios.post("/api/submit-review", payload)
            console.log(response.data)
            } catch (err) {
                console.error(err)
            }
     }

return(
    <div className="page">
        <form onSubmit={handleSubmit}>

            <div className="formfields">
                <label>Rating</label>
                <input value={rating} onChange={(e)=>
                    setRating(e.target.value)
                }/>

                <label>Comment</label>
                <input value={comment} onChange={(e)=>
                    setComment(e.target.value)
                }/>
            </div>
            <button type="submit" id="submit-btn">Submit</button>

        </form>
    </div>
)
}

export default PostReview
