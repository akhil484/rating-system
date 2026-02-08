import {useState, useEffect} from "react";
import axios from 'axios';
import { useParams } from "react-router-dom";
import StarRating from "../Star.jsx";
import './style.css'

function ProductReviews(){
    const { uid } = useParams();
    const [product, setProduct] = useState(null);
    const [reviews, setReviews] = useState([]);

    useEffect(() => {
        const loadProducts = async () => {
            try {
                const response = await axios.get(`/api/get-product/${uid}`);
                setReviews(response.data.ratings)
                setProduct(response.data)

            } catch (err) {
                console.error(err)
            }
        }

        loadProducts()
    }, [])


    useEffect(() => {
        const ws = new WebSocket(`ws://127.0.0.1:8000/ws/product/${uid}`);

        ws.onopen = () => {
            console.log('WebSocket Connected');
        };

        ws.onmessage = (event) => {
            console.log('on message 88888888888888')
            const data = JSON.parse(event.data);

            console.log(data)
            if (data.type === 'rating_update') {
                setReviews(prevReviews => [data.latest_review, ...prevReviews]);
            }
        }

        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
        ws.onclose = () => {
            console.log('WebSocket Disconnected');
        }
        return () => {
            ws.close();
        };
    }, [])

    return (
        <div className="box">
            <div className="container">
                {product &&
                    (<div key={product.id}>
                        <p id="p_name">{product.name}</p>
                    </div>)}
                {reviews?.length === 0 && <p>No Reviews</p>}
                {reviews?.map(review => (
                    <div key={review.id} className="allreviews">
                        <StarRating rating={review.rating} />
                        <p className="star-rating">{review.rating},</p>
                        <p className="comments">{review.comment}</p>

                    </div>
                ))}

            </div>
        </div>
    )
}

export default ProductReviews
