import {useState, useEffect} from "react";
import axios from 'axios';

function AllProducts(){
    const [products, setProducts] = useState([]);
    useEffect(() => {
        const loadProducts = async () => {
            try {
                const response = await axios.get("/api/get-products");
                setProducts(response.data)
            } catch (err) {
                console.error(err)
            }
        }

        loadProducts()
    }, [])


    return (
        <div>
            <h2>All Products</h2>
            {products.length === 0 && <p>No products</p>}

            {products.map(product => (
                <div key={product.id}>
                    <a href={`/product/${product.uid}`}><strong>{product.name}</strong></a>
                </div>
            ))}
        </div>
    )
}

export default AllProducts
