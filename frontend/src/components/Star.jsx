import { FaStar } from "react-icons/fa";

const Star = ({ fill }) => (
  <div style={{ position: "relative", width: 20, height: 20 }}>
    <FaStar size={20} color="#ccc" />
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: `${fill}%`,
        overflow: "hidden",
      }}
    >
      <FaStar size={20} color="#FFCD69" />
    </div>
  </div>
);

const StarRating = ({ rating, totalStars = 5 }) => {
  return (
    <div style={{ display: "flex", gap: 4 }}>
      {[...Array(totalStars)].map((_, i) => {
        const fill = Math.max(
          0,
          Math.min(100, (rating - i) * 100)
        );
        return <Star key={i} fill={fill} />;
      })}
    </div>
  );
};
export default StarRating;