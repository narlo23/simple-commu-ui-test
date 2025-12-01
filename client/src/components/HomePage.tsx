import { useAuth } from "./AuthContext";
import { useQuery } from "@tanstack/react-query";
import PostCard, { Post } from "./PostCard";
import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { MessageSquare } from "lucide-react";

export default function HomePage() {
  const { user, isAuthenticated } = useAuth();

  const { data: posts, isLoading, error } = useQuery<Post[]>({
    queryKey: ["/api/posts", { limit: 5 }],
    queryFn: async () => {
      const response = await fetch("/api/posts?limit=5");
      if (!response.ok) throw new Error("Failed to fetch posts");
      return response.json();
    },
  });

  return (
    <div className="mx-auto max-w-4xl px-4 py-8">
      <div className="mb-8">
        <h1 className="mb-2 text-3xl font-bold md:text-4xl">
          {isAuthenticated ? (
            <>Welcome back, <span className="text-primary" data-testid="text-welcome-username">{user?.username}</span></>
          ) : (
            "Welcome to Vanilla Community"
          )}
        </h1>
        <p className="text-muted-foreground">
          {isAuthenticated
            ? "Here are the latest posts from our community"
            : "Join our community to share and discover great content"}
        </p>
      </div>

      <section>
        <h2 className="mb-4 flex items-center gap-2 text-xl font-semibold">
          <MessageSquare className="h-5 w-5 text-primary" />
          Recent Posts
        </h2>

        <div className="space-y-4" data-testid="container-posts-list">
          {isLoading ? (
            <>
              {[1, 2, 3, 4, 5].map((i) => (
                <Card key={i}>
                  <CardContent className="p-6">
                    <Skeleton className="mb-4 h-6 w-3/4" />
                    <Skeleton className="mb-2 h-4 w-full" />
                    <Skeleton className="mb-4 h-4 w-2/3" />
                    <div className="flex gap-4">
                      <Skeleton className="h-4 w-24" />
                      <Skeleton className="h-4 w-24" />
                    </div>
                  </CardContent>
                </Card>
              ))}
            </>
          ) : error ? (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12 text-center">
                <MessageSquare className="mb-4 h-12 w-12 text-muted-foreground" />
                <h3 className="mb-2 text-lg font-semibold">Error loading posts</h3>
                <p className="text-muted-foreground">
                  Something went wrong. Please try again later.
                </p>
              </CardContent>
            </Card>
          ) : posts && posts.length > 0 ? (
            posts.map((post) => <PostCard key={post.id} post={post} />)
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12 text-center">
                <MessageSquare className="mb-4 h-12 w-12 text-muted-foreground" />
                <h3 className="mb-2 text-lg font-semibold">No posts yet</h3>
                <p className="text-muted-foreground">
                  Be the first to share something with the community!
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </section>
    </div>
  );
}
